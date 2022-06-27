import json
import traceback
import logging
from os import PathLike
from pathlib import Path
from typing import List

import requests

# setup a basic logging config if one isn't already set
logging.basicConfig(level="info")

class BugSplat:
    def __init__(self,
                 database: str,
                 application: str,
                 version: str,
                 logger: logging.Logger = None):
        self.database = database
        self.application = application
        self.version = version
        self.additional_file_paths = []
        self.app_key = ''
        self.description = ''
        self.email = ''
        self.user = ''
        self.logger = logger or logging.getLogger(__name__)

    def set_default_additional_file_paths(self, additional_file_paths: List[PathLike]):
        self.additional_file_paths = additional_file_paths

    def set_default_app_key(self, key: str):
        self.app_key = key

    def set_default_description(self, description: str):
        self.description = description

    def set_default_email(self, email: str):
        self.email = email

    def set_default_user(self, user: str):
        self.user = user

    def post(self,
             ex: BaseException or str,
             additional_file_paths: List[PathLike] = None,
             app_key: str = '',
             description: str = '',
             email: str = '',
             user: str = ''):

        if not additional_file_paths:
            additional_file_paths = self.additional_file_paths

        self.logger.info('\nBugSplat caught an Unhandled Exception!\n')

        # TODO BG what if ex is not defined? Do we care?
        # https://stackoverflow.com/q/3702675/4272428
        callstack = self._convert_exception_to_json(ex)

        self.logger.info(f'About to post crash to database {self.database}...\n')

        url = f'https://{self.database}.bugsplat.com/post/py/'
        files = self._create_files_for_post(additional_file_paths)

        data = {
            'database': self.database,
            'appName': self.application,
            'appVersion': self.version,
            'appKey': app_key or self.app_key,
            'description': description or self.description,
            'exceptionMessage': str(ex),
            'email': email or self.email,
            'user': user or self.user,
            'callstack': callstack
        }

        try:
            response = requests.post(url, files=files, data=data)

            if response.status_code != 200:
                raise Exception(
                    f'Status: {response.status_code} \n Message: {response.text}'
                )

            self.logger.info('Crash posted successfully!')
        except Exception as ex:
            self.logger.exception('Crash post failed!', exc_info=ex)

    @staticmethod
    def _convert_exception_to_json(ex: BaseException):
        def frame_summary_to_dict(s: traceback.FrameSummary):
            return {
                'filename': s.filename,
                'line': s.line,
                'lineno': s.lineno,
                'locals': s.locals,
                'name': s.name
            }

        tb = traceback.TracebackException.from_exception(ex, capture_locals=True)

        return json.dumps([frame_summary_to_dict(t) for t in tb.stack])

    @staticmethod
    def _create_files_for_post(paths: List[PathLike]):
        files = {}

        for p in paths:
            name = Path(p).name
            files[name] = open(p, 'rb')

        return files

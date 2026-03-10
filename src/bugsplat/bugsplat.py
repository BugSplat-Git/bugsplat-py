import io
import json
import traceback
import logging
import zipfile
from os import PathLike
from pathlib import Path
from typing import List

import requests

# setup a basic logging config if one isn't already set
logging.basicConfig(level=logging.INFO)

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

    def post_feedback(self,
                      title: str,
                      description: str = '',
                      email: str = '',
                      user: str = '',
                      app_key: str = ''):
        """Post user feedback to BugSplat using the presigned URL upload flow.

        Args:
            title: Feedback title, used as the stack key for grouping in the dashboard.
            description: Additional feedback context.
            email: Email of the user submitting feedback.
            user: Name or id of the user submitting feedback.
            app_key: Application key for support response page variation.
        """
        if not title:
            self.logger.error('Error: title cannot be empty when posting feedback to BugSplat')
            return

        self.logger.info(f'About to post feedback to database {self.database}...\n')

        base_url = f'https://{self.database}.bugsplat.com'

        # Create feedback.json and zip it
        feedback_json = json.dumps({'title': title, 'description': description or self.description})
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('feedback.json', feedback_json)
        zip_data = zip_buffer.getvalue()

        try:
            # Step 1: Get presigned upload URL
            get_url_params = {
                'database': self.database,
                'appName': self.application,
                'appVersion': self.version,
                'crashPostSize': len(zip_data)
            }
            get_url_response = requests.get(f'{base_url}/api/getCrashUploadUrl', params=get_url_params)
            get_url_response.raise_for_status()
            presigned_url = get_url_response.json()['url']

            # Step 2: Upload zip to S3
            put_response = requests.put(
                presigned_url,
                data=zip_data,
                headers={'Content-Type': 'application/zip'}
            )
            put_response.raise_for_status()
            etag = put_response.headers.get('ETag', '').strip('"')

            # Step 3: Commit the upload
            commit_data = {
                'database': self.database,
                'appName': self.application,
                'appVersion': self.version,
                'crashTypeId': '36',
                's3Key': presigned_url,
                'md5': etag,
                'description': description or self.description,
                'email': email or self.email,
                'user': user or self.user,
                'appKey': app_key or self.app_key,
            }
            commit_response = requests.post(f'{base_url}/api/commitS3CrashUpload', data=commit_data)
            commit_response.raise_for_status()

            self.logger.info('Feedback posted successfully!')
        except Exception as ex:
            self.logger.exception('Feedback post failed!', exc_info=ex)

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

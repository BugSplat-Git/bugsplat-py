import json
import os
import requests
import traceback
import sys

class BugSplat:
    def __init__(self, database, application, version):
        self.database = database
        self.application = application
        self.version = version
        self.additionalFilePaths = []
        self.appKey = ''
        self.description = ''
        self.email = ''
        self.user = ''

    def setDefaultAdditionalFilePaths(self, additionalFilePaths):
        self.additionalFilePaths = additionalFilePaths

    def setDefaultAppKey(self, key):
        self.appKey = key

    def setDefaultDescription(self, description):
        self.description = description
            
    def setDefaultEmail(self, email):
        self.email = email

    def setDefaultUser(self, user):
        self.user = user

    def post(self, ex, additionalFilePaths = [], appKey = '', description = '', email = '', user = ''):
        print('\n')
        print('BugSplat caught an Unhandled Exception!')
        print('\n')

        # TODO BG what if ex is not defined? Do we care?
        # https://stackoverflow.com/questions/3702675/how-to-catch-and-print-the-full-exception-traceback-without-halting-exiting-the
        callstack = self._convertExceptionToJson(ex)
        exceptionMessage = str(ex)

        print('About to post crash to database ' + self.database + '...')
        print('\n')

        url = 'https://' + self.database + '.bugsplat.com/post/py/'
        if (not appKey): appKey = self.appKey
        if (not description): description = self.description
        if (not email): email = self.email
        if (not user): user = self.user
        if (len(additionalFilePaths) == 0): additionalFilePaths = self.additionalFilePaths
        files = self._createFilesForPost(additionalFilePaths)

        data = {
            'database': self.database,
            'appName': self.application,
            'appVersion': self.version,
            'appKey': appKey,
            'description': description,
            'exceptionMessage': exceptionMessage,
            'email': email,
            'user': user,
            'callstack': callstack
        }

        try:
            response = requests.post(url, files = files, data = data)

            if (response.status_code !=  200):
                raise Exception('Status: ' + str(response.status_code) + '\n' + 'Message: ' + response.text)

            print('Crash posted successfully!')
        except Exception as ex:
            print('Crash post failed!')
            print('\n')
            print(ex)

    def _convertExceptionToJson(self, ex): 
        stack = []
        tb = traceback.TracebackException.from_exception(ex, capture_locals=True)
        
        for t in tb.stack:
            stack.append({
                'filename': t.filename,
                'line': t.line,
                'lineno': t.lineno,
                'locals': t.locals,
                'name': t.name
            })

        return json.dumps(stack)

    def _createFilesForPost(self, paths):
        files = {}

        for p in paths:
            name = os.path.basename(p)
            files[name] = open(p, 'rb')
            
        return files
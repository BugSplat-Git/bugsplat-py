import os
import pathlib
import sys
from bugsplat import BugSplat
from helpers import crash

here = pathlib.Path(__file__).parent.resolve()
additionalFilePath = os.path.join(here, 'attachment.txt')
additionalFilePath2 = os.path.join(here, 'attachment2.txt')

bugsplat = BugSplat('fred', 'my-python-crasher', '1.0.0')
bugsplat.set_default_app_key('key!')
bugsplat.set_default_description('description!')
bugsplat.set_default_email('fred@bugsplat.com')
bugsplat.set_default_user('Fred')
bugsplat.setDefaultAdditionalFilePaths([
    additionalFilePath,
    additionalFilePath2
])

try:
    crash()
except Exception as e:
    bugsplat.post(e, app_key='other key!', description='other description!', email='barney@bugsplat.com', user ='Barney')

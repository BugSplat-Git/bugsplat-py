import os
import pathlib
import sys
from bugsplat import BugSplat
from helpers import crash

here = pathlib.Path(__file__).parent.resolve()
additionalFilePath = os.path.join(here, 'attachment.txt')

bugsplat = BugSplat('fred', 'my-python-crasher', '1.0.0')
bugsplat.setDefaultAppKey('key!')
bugsplat.setDefaultDescription('description!')
bugsplat.setDefaultEmail('fred@bugsplat.com')
bugsplat.setDefaultUser('Fred')
bugsplat.setDefaultAdditionalFilePaths([additionalFilePath])

try:
    crash()
except Exception as e:
    bugsplat.post(e, appKey='other key!', description='other description!', email='barney@bugsplat.com', user = 'Barney')

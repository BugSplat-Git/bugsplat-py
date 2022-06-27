from pathlib import Path
from bugsplat import BugSplat
from helpers import crash

cwd = Path(__file__).parent

additional_file_paths = [
    cwd / 'attachment.txt',
    cwd / 'attachment2.txt'
]

bugsplat = BugSplat('fred', 'my-python-crasher', '1.0.0')
bugsplat.set_default_app_key('key!')
bugsplat.set_default_description('description!')
bugsplat.set_default_email('fred@bugsplat.com')
bugsplat.set_default_user('Fred')
bugsplat.set_default_additional_file_paths(additional_file_paths)

try:
    crash()
except Exception as e:
    bugsplat.post(
        e, 
        app_key='other key!', 
        description='other description!', 
        email='barney@bugsplat.com', 
        user ='Barney'
    )

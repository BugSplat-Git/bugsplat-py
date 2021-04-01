# bugsplat-py

A BugSplat integration for reporting Unhandled Exceptions in Python.

## Installing
Install the bugsplat package using pip
```shell
pip install bugsplat
```

## Usage
1. Import the BugSplat class
```python
from bugsplat import BugSplat
```
2. Create a new BugSplat instance passing it the name of your BugSplat database, application and version
```python
bugsplat = BugSplat(database, application, version)
```
3. Optionally, you set default values for appKey, description, email and user
```python
bugsplat.setDefaultAppKey('key!')
bugsplat.setDefaultDescription('description!')
bugsplat.setDefaultEmail('fred@bugsplat.com')
bugsplat.setDefaultUser('Fred')
```
4. Wrap your application code in a try except block. In the except block call post. You can override any of the default properties that were set in step 3
```python
try:
    crash()
except Exception as e:
    bugsplat.post(e, appKey='other key!', description='other description!', email='barney@bugsplat.com', user = 'Barney')
```
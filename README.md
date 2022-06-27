[![bugsplat-github-banner-basic-outline](https://user-images.githubusercontent.com/20464226/149019306-3186103c-5315-4dad-a499-4fd1df408475.png)](https://bugsplat.com)
<br/>
# <div align="center">BugSplat</div> 
### **<div align="center">Crash and error reporting built for busy developers.</div>**
<div align="center">
    <a href="https://twitter.com/BugSplatCo">
        <img alt="Follow @bugsplatco on Twitter" src="https://img.shields.io/twitter/follow/bugsplatco?label=Follow%20BugSplat&style=social">
    </a>
    <a href="https://discord.gg/K4KjjRV5ve">
        <img alt="Join BugSplat on Discord" src="https://img.shields.io/discord/664965194799251487?label=Join%20Discord&logo=Discord&style=social">
    </a>
</div>

## 👋 Introduction

This repo contains the source code for bugsplat-py, a BugSplat integration for reporting Unhandled Exceptions in Python.

## 🏗 Installation

Install the bugsplat package using pip

```shell
pip install bugsplat
```

## ⚙️ Configuration

1. Import the BugSplat class

```python
from bugsplat import BugSplat
```

2. Create a new BugSplat instance passing it the name of your BugSplat database, application and version

```python
bugsplat = BugSplat(database, application, version)
```

3. Optionally, you set default values for appKey, description, email, user and additionaFilePaths

```python
bugsplat.setDefaultAppKey('key!')
bugsplat.setDefaultDescription('description!')
bugsplat.setDefaultEmail('fred@bugsplat.com')
bugsplat.setDefaultUser('Fred')
bugsplat.setDefaultAdditionalFilePaths([
    './path/to/additional-file.txt',
    './path/to/additional-file-2.txt'
])
```

4. Wrap your application code in a try except block. In the except block call post. You can override any of the default properties that were set in step 3

```python
try:
    crash()
except Exception as e:
    bugsplat.post(
        e, 
        additionalFilePaths=[], 
        appKey='other key!', 
        description='other description!', 
        email='barney@bugsplat.com', 
        user='Barney'
    )
```

5. Once you've posted a crash, navigate to the Crashes page and click the link in the ID column to be see the crash's details

<img width="1713" alt="BugSplat Crash Page" src="https://user-images.githubusercontent.com/2646053/175091507-32a9c505-1d26-4d5b-aef7-44b5a347ddb4.png">

## 🧑‍💻 Development

To configure a development environment:

1. Clone the repository

```shell
git clone https://github.com/BugSplat-Git/bugsplat-py.git
```

2. Create a virtual environment

```shell
python -m venv venv
```

3. Activate the virtual environment

```shell
# unix/macos
source venv/bin/activate

# windows
.\env\Scripts\activate
```

4. Install the project's dependencies

```shell
pip install .
```

Thanks for using BugSplat ❤️

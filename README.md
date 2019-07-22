Projects Overview

Portable project explorer
Abstraction above file system

# TODO: Project explorer stuff
# TODO: Archive projects, upload to AWS
# AWS keys need to be embeded somewhere? Should this be an api request?
# auto updating? Maybe the logic and ui is pulled from aws on load?
# TODO: project checker
# TODO: collect scene

quick way to get qtdesigner
--

Install the latest version of "pyqt5-tools" using pip install pyqt5-tools --pre

The "designer.exe" will be installed in ...Lib\site-packages\pyqt5_tools

https://stackoverflow.com/questions/30222572/how-to-install-qtdesigner



Compile exe
--

```
$ cd \po\po
```

```
$ pipenv install
$ pipenv shell
```

```
$ pyinstaller --onefile --noconsole app.py
```

Or, if no _app.spec file is present run the below. However this method might not
load UI files.

```
$ pyinstaller --onefile --noconsole app.py
```

Exe will be located in \po\po\dist\app.exe
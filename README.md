
# Prerequisite Setup
## Install wasmer and wapm

```shell
$ brew install wasmer
$ brew install wapm
$ wapm install python/python
```

This will result in a wapm_packages directory in your project folder.

## Setup your python environment

create a virtual environment as you would normally do
```shell
python -m venv .venv
```

activate the virtual environment
```shell
$ source .venv/bin/activate
```

install packages
```shell
$ cd requirements
$ ./pip-install.sh
```

# Run the example

Run the example_sandbox.py file
```python
$ python example_sandbox.py
wasi stdout
WARNING: this string is the result of executing unknown code, so be careful how you use it!
####
Hello, world!
####
```

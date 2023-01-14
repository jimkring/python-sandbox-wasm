# Python Sandbox in Web Assembly (wasm)

This is proof-of-concept for executing python code in a sandboxed web assembly (wasm) build of python.
It uses wasmer-python to  run the wasm build of python and wapm to install the python package.

## Resources
### starting point example
https://github.com/wasmerio/wasmer-python/blob/master/examples/wasi.py

### wasmer-python
https://github.com/wasmerio/wasmer-python

### wapm python.wam package
https://wapm.io/python/python

## Prerequisite Setup
### Install wasmer and wapm

```shell
$ brew install wasmer
$ brew install wapm
$ wapm install python/python
```

This will result in a wapm_packages directory in your project folder.

### Setup your python environment

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
$ pip install -r requirements/requirements.txt
```

## Running the example

Run the example_sandbox.py file
```python
$ python example_sandbox.py
wasi stdout
WARNING: this string is the result of executing unknown code, so be careful how you use it!
####
Hello, world!
####
```

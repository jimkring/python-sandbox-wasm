# Python Sandbox in Web Assembly (wasm)

This is proof-of-concept for executing python code in a sandboxed web assembly (wasm) build of python.
It uses wasmer-python to  run the wasm build of python and wapm to install the python package.

[![Setup and Test](https://github.com/jimkring/python-sandbox-wasm/actions/workflows/python-app.yml/badge.svg)](https://github.com/jimkring/python-sandbox-wasm/actions/workflows/python-app.yml)

## How it all works

- From our host python we use the [wasmer-python](https://github.com/wasmerio/wasmer-python) library to load and run the [python web assembly](https://wapm.io/python/python) (wasm) from wapm (web assembly package manager).

- we create a "sandbox" folder that is shared with the web assembly python instance.

- we take the unsafe python code (to be executed in the sandbox) and write it to a python file in the sandbox folder. We prepend to that file a few lines of code that will write the standard output (stdout) to a file in the sandbox folder (which we will then read back into the host python instance).

- we run the python web assembly instance with the sandboxed python file we just created as the argument, so that the unsafe code runs inside the web assembly instance.

- we then read the standard output file from the sandbox folder and return it to the host python instance.

> Note: it does not seem possible to redirect the std output of the web assembly to file FROM THE HOST PYTHON.  This only works from the python code running inside the web assembly. That's why we have to prepend the unsafe code with a few lines of code that will write the std output to a file.

## Resources
Tools and examples used here:

- starting point example: https://github.com/wasmerio/wasmer-python/blob/master/examples/wasi.py
- wasmer-python: https://github.com/wasmerio/wasmer-python
- wapm python.wam package: https://wapm.io/python/python

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

# Future Needs

## Calling into Python C API

It would be great to be able call into the python web assembly using functions/exports from the [python c api](https://docs.python.org/3/c-api/) that expose the interpreter. Right now, we are invoking the `_start()` which is like running python from a command line -- we can pass arguments and set environment variables as we run it.

This would require a new build of the python.wasm possibly building it as a dynamic library. The nodjs package [python-wasm](https://www.npmjs.com/package/python-wasm) for embedding python takes an approach like this, I believe.

## Configurable Resource Limits (RAM, Disk, CPU, etc)

It would be good to limit the resources available to the sandboxed code. Wasmer (and the wasmer python api) exposes some options for this, I believe.

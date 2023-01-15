# Python Sandbox in Web Assembly (wasm)

This is proof-of-concept for executing python code in a sandboxed web assembly (wasm) build of python.
It uses wasmer-python to  run the wasm build of python and wapm to install the python package.

[![Setup and Test](https://github.com/jimkring/python-sandbox-wasm/actions/workflows/python-app.yml/badge.svg)](https://github.com/jimkring/python-sandbox-wasm/actions/workflows/python-app.yml)

Compatibility:

- OS: Linux, MacOS, and Windows (tested on ubuntu-latest, macos-latest and windows-latest github runners)
- Python: 3.7, 3.8, 3.9 and 3.10 (tested with standard cpython [actions/setup-python](https://github.com/actions/setup-python))

Incompatibility:

- NOT WORKING WITH python 3.11 (seems wasm-python library does not support 3.11 yet, as of Jan 14, 2023)

## How it All Works

- From our host python we use the [wasmer-python](https://github.com/wasmerio/wasmer-python) library to load and run the [python web assembly](https://wapm.io/python/python) (wasm) from wapm (web assembly package manager).

- we create a "sandbox" folder that is shared with the web assembly python instance.

- we take the unsafe python code (to be executed in the sandbox) and write it to a python file in the sandbox folder. We prepend to that file a few lines of code that will write the standard output (stdout) to a file in the sandbox folder (which we will then read back into the host python instance).

- we run the python web assembly instance with the sandboxed python file we just created as the argument, so that the unsafe code runs inside the web assembly instance.

- we then read the standard output file from the sandbox folder and return it to the host python instance.

> Note: it does not seem possible to redirect the std output of the web assembly to file FROM THE HOST PYTHON.  This only works from the python code running inside the web assembly. That's why we have to prepend the unsafe code with a few lines of code that will write the std output to a file.

## Useful Resources
Tools and examples used here:

- [starting point example](https://github.com/wasmerio/wasmer-python/blob/master/examples/wasi.py) - this was the starting point for this project/code ([example_sandbox.py](https://github.com/jimkring/python-sandbox-wasm/blob/main/example_sandbox.py))
- [wasmer-python](https://github.com/wasmerio/wasmer-python) - the python library that we use to load/compile/run the python.wasm and our sandboxed python script
- [wapm python.wasm package](https://wapm.io/python/python) - the python web assembly package that installs python.wasm into our project folder so we can call it with wasmer.

## Required Tools and Setup

### Install wasmer and wapm

Again, wasmer is the web assembly runtime and wapm is the web assembly package manager that will install the python web assembly package.

On MacOS with homebrew
```shell
$ brew install wasmer
$ brew install wapm
```

From the instructions on [wasmer.io](https://wasmer.io/)
```shell
$ curl https://get.wasmer.io -sSfL | sh
```

### Install python web assembly using wapm

```shell
$ wapm install python/python
```

This will result in a wapm_packages directory in your project folder, which contains python compiled as a web assembly.

### Setup your python environment

We're not going to setup our "host" python environment that will run our safe/trusted code.

create a virtual environment as you would normally do (this is just and example using `venv`)
```shell
python -m venv .venv
```

activate the virtual environment (if you are using one)
```shell
$ source .venv/bin/activate
```

install packages in the [requirements.txt](https://github.com/jimkring/python-sandbox-wasm/blob/main/requirements/requirements.txt) file
```shell
$ pip install -r requirements/requirements.txt
```

## Run the example

Run the example_sandbox.py file
```python
$ python example_sandbox.py
wasi stdout
WARNING: this string is the result of executing unknown code, so be careful how you use it!
####
Hello, world!
####
```

> Note: You can see the code run in [this GitHub action](https://github.com/jimkring/python-sandbox-wasm/actions/workflows/python-app.yml) workflow that tests it. You can verify it's working because you can see the example output:

<img width="500" alt="image" src="https://user-images.githubusercontent.com/381432/212523083-334f1e4d-e8e3-4553-84d5-5073bea3f53c.png">

# Future Needs (Roadmap?)

## Calling into Python C API

It would be great to be able call into the python web assembly using functions/exports from the [python c api](https://docs.python.org/3/c-api/) that expose the interpreter. Right now, we are invoking the `_start()` which is like running python from a command line -- we can pass arguments and set environment variables as we run it.

This would require a new build of the python.wasm possibly building it as a dynamic library. The nodjs package [python-wasm](https://www.npmjs.com/package/python-wasm) for embedding python takes an approach like this, I believe.

## Configurable Resource Limits (RAM, Disk, CPU, etc)

It would be good to limit the resources available to the sandboxed code. Wasmer (and the wasmer python api) exposes some options for this, I believe.

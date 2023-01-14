"""
Execute python code in a sandboxed python web assembly.
"""
import os
from pathlib import Path

from wasmer.wasmer import ImportObject, Instance, Module, Store, engine, wasi
from wasmer_compiler_cranelift.wasmer_compiler_cranelift import Compiler

# Load the wasm as bytes
__dir__ = os.path.dirname(os.path.realpath(__file__))
wasm_bytes = open("wapm_packages/python/python@0.1.0/bin/python.wasm", "rb").read()

# Create a store.
store = Store(engine.Universal(Compiler))

# compile the wasm module
module = Module(store, wasm_bytes)

# Get the wasi version -- we'll need it below
wasi_version = wasi.get_version(module, strict=True)

# Create a `wasi.Environment` with the the `wasi.StateBuilder`.
#
# In this case, we specify the program name is `wasi_test_program`. We
# also specify the program is invoked with the `--test` argument, in
# addition to two environment variable: `COLOR` and
# `APP_SHOULD_LOG`. Finally, we map the `the_host_current_dir` to the
# current directory. There it is:

unsafe_python_code = """
print('Hello, world!')
"""

stdout_file = "out.txt"

# wrap python code, redirecting stdout to a file
wrapped_python_code = f"""

# redirect stdout to a file
import sys
sys.stdout = open("sandbox/{stdout_file}", "w")

# unsafe python code starts here
{unsafe_python_code}

"""


# Define sandbox directory. This and the "lib" dir are the only dirs 
# the wasm can access.
sandbox_dir = Path.cwd() / "sandbox"

# create sandbox dir if it doesn't exist
sandbox_dir.mkdir(exist_ok=True)

# Define the name of the python file to host the executable code
sandbox_py = "sandbox.py"

sandbox_py_path = sandbox_dir / sandbox_py

# delete sandbox py file if it exists
if sandbox_py_path.exists():
    sandbox_py_path.unlink()
    
sandbox_stdout_path = sandbox_dir / stdout_file

# delete sandbox stdout file if it exists
if sandbox_stdout_path.exists():
    sandbox_stdout_path.unlink()

# write the code to the sandbox
with open(sandbox_dir / sandbox_py, "w") as f:
    f.write(wrapped_python_code)

py_program_name = "python"
py_lib_dir = "wapm_packages/python/python@0.1.0/lib"
py_environment = {
    # 'VARIABLE': 'value',
}
py_arguments = [
    f"sandbox/{sandbox_py}",
]

# let's build the environment in a wasi state object
wasi_state = wasi.StateBuilder(py_program_name)

# set the command arguments
for arg in py_arguments:
    wasi_state.argument(arg)

# set the environment variables
for key, value in py_environment.items():
    wasi_state.environment(key, value)

# map the python lib directory
wasi_state.map_directory("lib", py_lib_dir)
wasi_state.map_directory("sandbox", str(sandbox_dir))

# # Create the in-memory "file"
# wasi_stdout = StringIO()

# wasi_state.set_stdout(wasi_stdout)

# finalize the environment
wasi_env = wasi_state.finalize()

# From the WASI environment, generate a custom, pre-configured import object.
#
# Note we need the WASI version here.
import_object = wasi_env.generate_import_object(store, wasi_version)

# Instantiate the module.
instance = Instance(module, import_object)

# # Redirect stdout to a file before running the WASI module (NOTE: this is NOT working!)
# with open("out.txt", "w") as f:
#     with redirect_stdout(f):
#         print(f"before wasi")

#         # The entry point for a WASI WebAssembly module is a function named `_start`
#         instance.exports._start()

# The entry point for a WASI WebAssembly module is a function named `_start`
instance.exports._start()

# read the sandbox's stdout into a string
# NOTE: this string is the result of executing unknown code, so be careful how you use it!)
with open(sandbox_stdout_path, "r") as f:
    wasi_stdout_unsafe = f.read()
    
print(
    f"wasi stdout\nWARNING: this string is the result of executing unknown code, "
    f"so be careful how you use it!\n####\n{wasi_stdout_unsafe}####"
)

# todo: move this to top of file
LEAVE_SANDBOX_FILES_FOR_DEBUG = False

# clean up sandbox files if we're not debugging
if not LEAVE_SANDBOX_FILES_FOR_DEBUG:
    sandbox_py_path.unlink()
    sandbox_stdout_path.unlink()
from cx_Freeze import setup, Executable
import sys
import os
import requests.certs


# base = "Win32GUI"
base = None

# base = None es con consola, base = "Win32GUI" es sin consola


executables = [Executable("main_to_execute.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages': packages,
        'include_files': [os.path.join(sys.base_prefix, 'DLLs', 'sqlite3.dll'),
                          (requests.certs.where(), 'cacert.pem'),
                          "ui/",
                          "data/"]
    },

}

setup(
    name="name",
    options=options,
    requires=["requests"],
    version="1",
    description='test',
    executables=executables
)

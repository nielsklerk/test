import cx_Freeze

executables = [cx_Freeze.Executable("PWS_code.py")]

cx_Freeze.setup(
    name="Re:birth",
    options={"build_exe": {"packages"}: [pygame],
"include_files": [img]}),
executables = executables

)

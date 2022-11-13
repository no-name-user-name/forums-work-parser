from cx_Freeze import setup, Executable

build_options = {'packages': [], 'excludes': []}

base = 'Console'

executables = [
    Executable('main.py', base=base, target_name='Zelenka Work Parer')
]

setup(name='ZelenkaWorkParer',
      version='1.0.0',
      description='',
      options={'build_exe': build_options},
      executables=executables)

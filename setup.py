import sys
import os
import cx_Freeze

base = None

# Definindo o caminho dos ícones e imagens usadas
os.environ['TCL_LIBRARY'] = r'C:\\Users\\Cleber Sena\AppData\\Local\\Programs\\Python\\Python312\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\\Users\\Cleber Sena\AppData\\Local\\Programs\\Python\\Python312\\tcl\\tk8.6'

if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("login.py", base=base, icon="icon.ico")]

cx_Freeze.setup(
    name="Sistema de Login",
    options={"build_exe": {"packages":["tkinter", "sqlite3", "os"],
                           "include_files":["login.png", "img-2-4k.png", "admin.ico"]}},
    version="1.0",
    description="Sistema de Login e Cadastro de Usuários",
    executables=executables
)

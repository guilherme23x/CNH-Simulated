import sys
from cx_Freeze import setup, Executable

# 1. Liste todas as pastas e arquivos extras que seu app precisa
build_exe_options = {
    "packages": ["os", "sys"], # Adicione bibliotecas extras aqui se necessário
    "include_files": [
        "assets/",
        "core/",
        "json/",
        "logic/",
        "ui/",
    ],
}

base = "gui" if sys.platform == "win32" else None

setup(
    name="CNH Simulated",
    version="1.0",
    description="Simulador CNH",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py", 
            base=base,
            icon="assets/car-icon.ico"
        )
    ],
)

import os
import sys
import importlib

print("INSTALL MODULES")

# قائمة المكتبات الأساسية فقط
REQUIRED_PACKAGES = {
    "telebot": "pyTelegramBotAPI",
    "kvsqlite": "kvsqlite",
    "schedule": "schedule",
    "requests": "requests",
    "user_agent": "user_agent",
    "aiosqlite": "aiosqlite",
    "telethon": "telethon",
    "pyrogram": "pyrogram",
}

def install(package):
    os.system(f"{sys.executable} -m pip install {package} --quiet")

def check_import(module_name, package_name=None):
    try:
        importlib.import_module(module_name)
        return True
    except:
        install(package_name or module_name)
        return False

# تثبيت المكتبات الأساسية
for module, package in REQUIRED_PACKAGES.items():
    check_import(module, package)

# مكتبات built-in (لا يتم تثبيتها!)
BUILTIN_MODULES = [
    "base64",
    "ipaddress",
    "struct",
    "pathlib",
    "typing",
    "secrets",
    "os",
    "sys"
]

print("DONE INSTALL MODULES")
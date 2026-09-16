#!/usr/bin/env python3
import os
import shutil
import sys
import platform
import ctypes
import tempfile
import subprocess

VERSION = "1.6.0"

# Residual build directories and target extension lists
PROJECT_GARBAGE_DIRS = {
    'build', '.dart_tool', '__pycache__', '.pytest_cache', 
    'node_modules', '.godot', 'dist', 'obj', '.cache',
    '.vs', 'DerivedData'
}

PROJECT_GARBAGE_EXTS = {
    '.tmp', '.log', '.pyc', '.pyo', '.spec', '.coverage',
    '.pdb', '.ilk', '.exp', '.lib'
}

# Carpetas que NUNCA deben explorarse ni modificarse bajo ninguna circunstancia
PROTECTED_DIR_NAMES = {
    'appdata',
    'program files',
    'program files (x86)',
    'windows',
    '$recycle.bin',
    'system volume information',
    '.vscode',
    '.android'
}

BANNER = r"""
  _____ _____    _    ____  _   _ _____ ____  
 |_   _|  _ \  / \  / ___|| | | | ____|  _ \ 
   | | | |_) |/ _ \ \___ \| |_| |  _| | |_) |
   | | |  _ < / ___ \ ___) |  _  | |___|  _ < 
   |_| |_| \_/_/   \_\____/|_| |_|_____|_| \_\
                 [DEV GARBAGE DEVOURER]
"""

def run_cmd(command):
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def smart_cli_clean(root_path):
    print("\n[TRASHER] Sniffing out environment clutter...")

    # Git Repositories
    if os.path.exists(os.path.join(root_path, ".git")):
        print("  [EAT] Pruning local Git database ('git gc')...")
        if run_cmd("git gc --prune=now"):
            print("  [OK] Git repository optimized.")

    # Pip Cache
    if shutil.which("pip") or shutil.which("pip3"):
        print("  [EAT] Purging global Python/Pip package cache...")
        run_cmd(f'"{sys.executable}" -m pip cache purge')
        print("  [OK] Pip cache purged.")

    # Docker
    if shutil.which("docker"):
        print("  [EAT] Cleaning dangling Docker containers and images...")
        if run_cmd("docker system prune -f"):
            print("  [OK] Docker resources purged.")

def clean_system_temp():
    temp_dir = tempfile.gettempdir()
    print(f"\n[TRASHER] Purging system Temp directory ({temp_dir})...")
    files_deleted = 0
    
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for f in files:
            try:
                os.remove(os.path.join(root, f))
                files_deleted += 1
            except Exception:
                pass
        for d in dirs:
            try:
                shutil.rmtree(os.path.join(root, d))
            except Exception:
                pass
                
    print(f"  [OK] Devoured {files_deleted} temporary files.")

def clean_project_files(root_path):
    print(f"\n[TRASHER] Shredding target directory: {os.path.abspath(root_path)}")
    deleted_files = 0
    deleted_dirs = 0

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        # CORTAFUEGOS: Elimina las carpetas protegidas del mapa de os.walk ANTES de entrar
        dirnames[:] = [d for d in dirnames if d.lower() not in PROTECTED_DIR_NAMES]

        # 1. Eliminar carpetas basura de proyectos
        for d in list(dirnames):
            if d.lower() in PROJECT_GARBAGE_DIRS:
                full_path = os.path.join(dirpath, d)
                try:
                    shutil.rmtree(full_path)
                    print(f"  [DELETED DIR] {full_path}")
                    deleted_dirs += 1
                    dirnames.remove(d)  # Evita intentar entrar a lo que se acaba de borrar
                except Exception:
                    pass

        # 2. Eliminar archivos temporales de compilación
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in PROJECT_GARBAGE_EXTS:
                full_path = os.path.join(dirpath, f)
                try:
                    os.remove(full_path)
                    print(f"  [DELETED FILE] {full_path}")
                    deleted_files += 1
                except Exception:
                    pass

    print(f"  [OK] Removed {deleted_dirs} directories and {deleted_files} junk files.")

def empty_trash():
    print("\n[TRASHER] Emptying System Trash / Recycle Bin...")
    system = platform.system()
    try:
        if system == "Windows":
            SHERB_NOCONFIRMATION = 0x00000001
            SHERB_NOPROGRESSUI = 0x00000002
            SHERB_NOSOUND = 0x00000004
            ctypes.windll.shell32.SHEmptyRecycleBinW(
                None, None, SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND
            )
            print("  [OK] Windows Recycle Bin emptied.")
        elif system == "Linux":
            trash_path = os.path.expanduser("~/.local/share/Trash")
            if os.path.exists(trash_path):
                shutil.rmtree(trash_path)
                os.makedirs(trash_path)
                print("  [OK] Linux Trash emptied.")
    except Exception as e:
        print(f"  [WARNING] Could not empty Trash: {e}")

def godspeed():
    """Self-destruct sequence for TRASHER"""
    print("\n[GODSPEED] Initiating self-destruct sequence...")
    system = platform.system()
    py_bin = sys.executable
    
    if system == "Windows":
        cmd = (
            'start /b cmd /c "'
            'timeout /t 2 /nobreak >nul && '
            f'"{py_bin}" -m ensurepip --default-pip >nul 2>&1 && '
            f'"{py_bin}" -m pip uninstall -y trasher && '
            'echo [OK] TRASHER has been completely uninstalled."'
        )
        subprocess.Popen(cmd, shell=True)
    else:
        cmd = f'sleep 2 && "{py_bin}" -m pip uninstall -y trasher'
        subprocess.Popen(cmd, shell=True)

    print("  [OK] TRASHER is erasing itself from the system. Goodbye!")
    sys.exit(0)

def main():
    if len(sys.argv) < 2:
        print(BANNER)
        print("Usage:")
        print("  trasher eat         -> Eats junk in current directory and system temp")
        print("  trasher eat <path>  -> Eats junk in specified path")
        print("  trasher --version   -> Shows current version")
        print("  trasher godspeed    -> Self-destructs and uninstalls TRASHER")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd in ("--version", "-v", "version"):
        print(f"TRASHER v{VERSION}")
        sys.exit(0)
    elif cmd == "godspeed":
        godspeed()
    elif cmd == "eat":
        target_path = sys.argv[2] if len(sys.argv) > 2 else "."
        print(BANNER)
        smart_cli_clean(target_path)
        clean_project_files(target_path)
        clean_system_temp()
        empty_trash()
        print("\n=========================================")
        print(" [TRASHER HAS FINISHED FEASTING] ")
        print("=========================================\n")
    else:
        print(BANNER)
        print(f"Unknown command: {cmd}")
        print("Use 'trasher eat' or 'trasher godspeed'")
        sys.exit(1)

if __name__ == "__main__":
    main()

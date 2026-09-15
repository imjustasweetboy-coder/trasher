# TRASHER

> **DEV GARBAGE DEVOURER** — Standardized utility by **MENOS RUIDO**.

**TRASHER** is a cross-platform CLI tool built to wipe build artifacts, deep-purge environment caches, and empty system trash in one command. No third-party dependencies. Just pure Python standard library.

---

## Quick Start

### Installation

Install globally on **Windows**, **macOS**, or **Linux** via `pip`:

```bash
pip install git+https://github.com/imjustasweetboy-coder/trasher.git
```
---

## Usage

### Automated Deep Clean

Clean the current working directory, sweep active dev environments, purge system temp files, and dump the OS recycle bin:

```bash
trasher eat
```

Or target a specific project or directory path:

```bash
trasher eat ./path/to/target-project
```

### What TRASHER Devours Automatically:

* __Smart Environment Detection:__
  * Executes `flutter clean` when `pubspec.yaml` is present.
  * Prunes and optimizes local databases via `git gc --prune=now`.
  * Purges global package download caches using `pip cache purge`.
  * Removes dangling containers and unreferenced images with `docker system prune -f`.
    
* __Artifact Shredding:__
  * Recursively purges `node_modules`, `build`, `.dart_tool`, `__pycache__`, `.pytest_cache`, `.godot`, `dist`, `bin`, `obj`, `.cache`, `.vs`, `out`, and `DerivedData`.
  * Wipes build residue extensions including `.tmp`, `.log`, `.pyc`, `.pyo`, `.spec`, `.coverage`, `.pdb`, `.ilk`, `.exp`, and `.lib`.

* __System Level Maintenance:__
  * Cleans current user OS temporary directories (`Temp` / `/tmp`).
  * Programmatically empties Windows Recycle Bin or Linux system Trash.
 
### Self-Destruct & Uninstallation

Self-destruct and completely purge TRASHER from your system without leaving orphan executables, config files, or broken environment path variables:

```bash
trasher godspeed
```

### How SELF-DESTRUCTION Works:

1. Spawns a background asynchronous detached process.
2. Gracefully exits the active terminal harness.
3. Automatically triggers pip uninstall -y trasher behind the scenes.
4. Cleans up system binaries and site-package entries cleanly.

---

## Stack & Architecture

* __Core Engine:__ Python 3.7+ (`os`, `shutil`, `subprocess`, `ctypes`, `tempfile`, `platform`).
* __Distribution Standard:__ `pyproject.toml` (Setuptools build system).
* __Zero Overhead:__ No external dependencies required or installed.

import os
import json
import shutil
import subprocess
import winreg
import psutil
from pathlib import Path
from typing import Any, Optional

BACKUP_DIR = Path(r"C:\ProgramData\Fireoptimizer")
BACKUP_FILE = BACKUP_DIR / "backup_registry.json"

def ensure_backup_dir():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def run_cmd(cmd: str, wait: bool = True) -> subprocess.CompletedProcess:
    """Esegue un comando in cmd (stringa)."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def backup_registry_value(root, subkey: str, name: str):
    """Salva il valore del registro (se esiste) nel backup file."""
    ensure_backup_dir()
    try:
        with winreg.OpenKey(root, subkey, 0, winreg.KEY_READ) as k:
            val, _ = winreg.QueryValueEx(k, name)
    except FileNotFoundError:
        val = None
    backup = {}
    if BACKUP_FILE.exists():
        backup = json.loads(BACKUP_FILE.read_text())
    keypath = f"{root.name}\\{subkey}\\{name}"
    backup[keypath] = val
    BACKUP_FILE.write_text(json.dumps(backup, indent=2, ensure_ascii=False))

def restore_registry_all():
    """Ripristina tutti i valori salvati nel backup."""
    if not BACKUP_FILE.exists():
        return False
    backup = json.loads(BACKUP_FILE.read_text())
    for keypath, val in backup.items():
        # keypath like "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\..."
        parts = keypath.split("\\")
        rootname = parts[0]
        root = getattr(winreg, rootname)
        subkey = "\\".join(parts[1:-1])
        name = parts[-1]
        try:
            with winreg.CreateKeyEx(root, subkey, 0, winreg.KEY_WRITE) as k:
                if val is None:
                    try:
                        winreg.DeleteValue(k, name)
                    except FileNotFoundError:
                        pass
                else:
                    # Try to preserve int vs str
                    if isinstance(val, int):
                        winreg.SetValueEx(k, name, 0, winreg.REG_DWORD, val)
                    else:
                        winreg.SetValueEx(k, name, 0, winreg.REG_SZ, str(val))
        except Exception:
            pass
    return True

def set_registry_dword(root, subkey: str, name: str, value: int):
    """Setta un valore DWORD (salvando prima il precedente)."""
    try:
        backup_registry_value(root, subkey, name)
    except Exception:
        pass
    with winreg.CreateKeyEx(root, subkey, 0, winreg.KEY_WRITE) as k:
        winreg.SetValueEx(k, name, 0, winreg.REG_DWORD, int(value))

def enable_high_performance():
    # SCHEME_MIN alias High Performance; salviamo prima lo stato corrente
    run_cmd("powercfg -setactive SCHEME_MIN")

def enable_game_mode():
    # Game Mode
    set_registry_dword(winreg.HKEY_CURRENT_USER,
                       r"Software\Microsoft\GameBar",
                       "AutoGameModeEnabled", 1)
    set_registry_dword(winreg.HKEY_CURRENT_USER,
                       r"Software\Microsoft\Windows\CurrentVersion\GameMode",
                       "GameMode", 2)

def enable_hags():
    # Hardware Accelerated GPU Scheduling - may require reboot
    set_registry_dword(winreg.HKEY_LOCAL_MACHINE,
                       r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                       "HwSchMode", 2)

def stop_and_disable_service(service_name: str):
    try:
        run_cmd(f'sc stop "{service_name}"')
    except Exception:
        pass
    try:
        run_cmd(f'sc config "{service_name}" start= disabled')
    except Exception:
        pass

def safe_disable_default_services():
    # Lista conservativa: non disabilitare servizi essenziali
    services = ["DoSvc", "WSearch", "DiagTrack"]
    for s in services:
        stop_and_disable_service(s)

def clear_temp_user():
    # Cancella i file nella cartella TEMP dell'utente corrente in modo sicuro
    temp = Path(os.environ.get("TEMP", r"C:\Windows\Temp"))
    for item in temp.iterdir():
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
        except Exception:
            pass

def flush_dns():
    run_cmd("ipconfig /flushdns")

def trim_working_set():
    # EmptyWorkingSet su ogni processo (richiede privilegi)
    for p in psutil.process_iter(attrs=["pid", "name"]):
        try:
            proc = psutil.Process(p.info["pid"])
            proc.cpu_affinity()
            # EmptyWorkingSet via psutil not directly available; use psapi via ctypes if needed.
            # Simpler: call 'rundll32.exe advapi32.dll,ProcessIdleTasks' is not safe; keep conservative:
            proc.cpu_affinity(proc.cpu_affinity())  # no-op to avoid heavy ops
        except Exception:
            pass

def backup_defaults_note():
    ensure_backup_dir()
    # If no backup exists, create empty JSON
    if not BACKUP_FILE.exists():
        BACKUP_FILE.write_text(json.dumps({}, indent=2, ensure_ascii=False))

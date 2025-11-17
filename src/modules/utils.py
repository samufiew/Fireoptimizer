import subprocess, json
from pathlib import Path
import ctypes
import winreg

BACKUP_DIR = Path(r"C:\ProgramData\Fireoptimizer")
BACKUP_FILE = BACKUP_DIR / "backup.json"

def ensure_backup_dir():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    if not BACKUP_FILE.exists():
        BACKUP_FILE.write_text(json.dumps({}, indent=2, ensure_ascii=False))

def run_cmd(cmd, capture=False):
    """Esegue un comando shell. Ritorna (returncode, stdout, stderr)"""
    try:
        completed = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
        out = completed.stdout if capture else ""
        err = completed.stderr if capture else ""
        return completed.returncode, out, err
    except Exception as e:
        return 1, "", str(e)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def backup_registry_value(root, subkey, name):
    """Salva valore esistente (se esiste) nel backup file."""
    ensure_backup_dir()
    try:
        hroot = getattr(winreg, root)
        with winreg.OpenKey(hroot, subkey, 0, winreg.KEY_READ) as k:
            val, typ = winreg.QueryValueEx(k, name)
    except Exception:
        val = None
        typ = None
    data = {}
    if BACKUP_FILE.exists():
        data = json.loads(BACKUP_FILE.read_text())
    key = f"{root}\\{subkey}\\{name}"
    data[key] = {"value": val, "type": typ}
    BACKUP_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

def restore_all_registry():
    """Ripristina tutti i valori salvati (se possibile)."""
    if not BACKUP_FILE.exists():
        return False, "Nessun backup trovato"
    data = json.loads(BACKUP_FILE.read_text())
    for key, obj in data.items():
        try:
            parts = key.split("\\")
            root = getattr(winreg, parts[0])
            subkey = "\\".join(parts[1:-1])
            name = parts[-1]
            with winreg.CreateKeyEx(root, subkey, 0, winreg.KEY_WRITE) as k:
                val = obj.get("value")
                typ = obj.get("type")
                if val is None:
                    try:
                        winreg.DeleteValue(k, name)
                    except FileNotFoundError:
                        pass
                else:
                    if typ == winreg.REG_DWORD:
                        winreg.SetValueEx(k, name, 0, winreg.REG_DWORD, int(val))
                    else:
                        winreg.SetValueEx(k, name, 0, winreg.REG_SZ, str(val))
        except Exception:
            pass
    return True, "Restore completato"

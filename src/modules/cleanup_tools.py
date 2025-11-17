from modules.utils import run_cmd
from pathlib import Path
import shutil, os

def clear_temp_user():
    temp = Path(os.environ.get("TEMP", r"C:\Windows\Temp"))
    count = 0
    for item in temp.iterdir():
        try:
            if item.is_file():
                item.unlink()
                count += 1
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
                count += 1
        except Exception:
            pass
    return True, f"Items removed (approx): {count}"

def clean_softwaredistribution_download():
    # safe: only remove files inside SoftwareDistribution\Download (old update files)
    sd = Path(r"C:\Windows\SoftwareDistribution\Download")
    if not sd.exists():
        return False, "Folder not found"
    removed = 0
    for item in sd.iterdir():
        try:
            if item.is_file():
                item.unlink(); removed += 1
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True); removed += 1
        except Exception:
            pass
    return True, f"Deleted {removed} items from SoftwareDistribution\\Download"

def trim_memory_soft():
    # 'Soft' memory trim: call EmptyWorkingSet for a few accessible processes
    import psutil
    import ctypes
    import ctypes.wintypes
    psapi = ctypes.windll.psapi
    kernel = ctypes.windll.kernel32
    trimmed = 0
    for p in psutil.process_iter(attrs=['pid','name']):
        try:
            h = kernel.OpenProcess(0x001F0FFF, False, p.info['pid'])
            if h:
                psapi.EmptyWorkingSet(h)
                kernel.CloseHandle(h)
                trimmed += 1
        except Exception:
            pass
    return True, f"Attempted to trim working set on {trimmed} processes"

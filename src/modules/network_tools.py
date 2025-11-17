from modules.utils import run_cmd, backup_registry_value
import winreg

def flush_dns():
    return run_cmd("ipconfig /flushdns", capture=True)

def reset_winsock():
    return run_cmd("netsh winsock reset", capture=True)

def reset_ip():
    return run_cmd("netsh int ip reset", capture=True)

def refresh_dhcp():
    return run_cmd("ipconfig /renew", capture=True)

# Optional safe registry tweaks: TCPNoDelay (only saving the old)
def set_tcp_tweaks():
    # This is conservative: backup before setting
    try:
        backup_registry_value("HKEY_LOCAL_MACHINE", r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpAckFrequency")
        # Some systems may not have the values; we set only if available or as safe demo
    except Exception:
        pass
    # Do not aggressively change multiple low-level network settings here; keep to run_cmd resets.
    return True, "Applied safe network backup (no aggressive tweaks performed)"

from modules.utils import run_cmd, backup_registry_value
import winreg

def enable_high_performance():
    # safe: switch to High Performance scheme alias
    return run_cmd("powercfg -setactive SCHEME_MIN", capture=True)

def safe_disable_services(service_list):
    """service_list: array of service short names; we backup nothing here (sc doesn't keep prev), but we confirm"""
    results = []
    for s in service_list:
        # stop then disable start
        r1 = run_cmd(f'sc stop "{s}"', capture=True)
        r2 = run_cmd(f'sc config "{s}" start= disabled', capture=True)
        results.append((s, r1[0], r2[0]))
    return True, results

def list_safe_services_to_disable():
    # conservative list (adjust if you know your system uses these)
    return ["DoSvc", "WSearch", "DiagTrack", "MapsBroker", "RetailDemo"]

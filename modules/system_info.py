"""System information (CPU, RAM, Disk, Battery)"""
import psutil
import platform
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class SystemInfo:
    @staticmethod
    def get_all() -> str:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        lines = [
            f"💻 System Info:",
            f"  OS: {platform.system()} {platform.release()}",
            f"  CPU: {platform.processor()}",
            f"  CPU Usage: {cpu}%",
            f"  RAM: {ram.used//(1024**3)}GB / {ram.total//(1024**3)}GB ({ram.percent}%)",
            f"  Disk: {disk.used//(1024**3)}GB / {disk.total//(1024**3)}GB ({disk.percent}%)",
        ]
        try:
            battery = psutil.sensors_battery()
            if battery:
                lines.append(f"  Battery: {battery.percent}% {'(Charging)' if battery.power_plugged else '(Discharging)'}")
        except:
            pass
        return "\n".join(lines)

    @staticmethod
    def get_cpu() -> str:
        return f"CPU Usage: {psutil.cpu_percent(interval=1)}%"

    @staticmethod
    def get_ram() -> str:
        ram = psutil.virtual_memory()
        return f"RAM: {ram.percent}% used ({ram.used//(1024**3)}GB / {ram.total//(1024**3)}GB)"

    @staticmethod
    def get_battery() -> str:
        try:
            battery = psutil.sensors_battery()
            if battery:
                status = "Charging" if battery.power_plugged else "Discharging"
                return f"Battery: {battery.percent}% ({status}), {battery.secsleft//60} mins left"
            return "No battery detected"
        except Exception as e:
            return f"Battery error: {e}"

    @staticmethod
    def get_disk() -> str:
        disk = psutil.disk_usage('/')
        return f"Disk: {disk.percent}% used ({disk.free//(1024**3)}GB free)"

    @staticmethod
    def get_network() -> str:
        net = psutil.net_io_counters()
        return f"Network: Sent {net.bytes_sent//(1024**2)}MB, Received {net.bytes_recv//(1024**2)}MB"

    @staticmethod
    def list_processes(top: int = 10) -> str:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                procs.append(p.info)
            except:
                pass
        procs.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        lines = [f"Top {top} Processes:"]
        for p in procs[:top]:
            lines.append(f"  {p['pid']}: {p['name']} ({p['cpu_percent']}%)")
        return "\n".join(lines)

    @staticmethod
    def kill_process(name: str) -> str:
        killed = []
        for p in psutil.process_iter(['pid', 'name']):
            try:
                if name.lower() in p.info['name'].lower():
                    psutil.Process(p.info['pid']).terminate()
                    killed.append(p.info['name'])
            except:
                pass
        return f"Killed: {', '.join(killed)}" if killed else f"No process named '{name}' found"

"""
windows_api.py
Educational Ransomware Simulation - Windows API Demonstration
FOR EDUCATIONAL USE ONLY - Run only in isolated VM
"""

import ctypes
import ctypes.wintypes
import os
import logging
import subprocess
from pathlib import Path

class WindowsAPIHandler:
    """
    Demonstrates Windows API usage in ransomware.
    """
    
    def __init__(self):
        # Load Windows DLLs
        self.kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        self.advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Windows API constants
        self.DRIVE_FIXED = 3
        self.DRIVE_REMOTE = 4
        self.DRIVE_CDROM = 5
        self.DRIVE_RAMDISK = 6
    
    def detect_virtualization(self):
        """
        Detects if running in a VM (for safety).
        """
        vm_indicators = []
        
        # Method 1: Check for VM-specific files/drivers
        vm_files = [
            "C:\\windows\\System32\\drivers\\vmmouse.sys",
            "C:\\windows\\System32\\drivers\\vmhgfs.sys",
            "C:\\windows\\System32\\drivers\\vboxguest.sys",
        ]
        
        for pattern in vm_files:
            if os.path.exists(pattern):
                vm_indicators.append(f"VM file: {pattern}")
        
        # Method 2: Check MAC address prefixes
        try:
            output = subprocess.check_output("getmac", shell=True).decode()
            vm_macs = ['080027', '005056', '000569', '001C42']
            for mac in vm_macs:
                if mac in output:
                    vm_indicators.append(f"VM MAC prefix: {mac}")
        except:
            pass
        
        # Method 3: Check running processes
        try:
            output = subprocess.check_output("tasklist", shell=True).decode()
            vm_processes = ['vboxservice', 'vboxtray', 'vmtoolsd', 'vmwaretray']
            for proc in vm_processes:
                if proc.lower() in output.lower():
                    vm_indicators.append(f"VM process: {proc}")
        except:
            pass
        
        if vm_indicators:
            self.logger.info("[VM DETECTION] VM indicators found")
            return True
        else:
            self.logger.info("[VM DETECTION] No VM indicators found")
            return False
    
    def get_drives_to_encrypt(self):
        """
        Use GetDriveTypeW API to identify drives.
        """
        drives = []
        bitmask = self.kernel32.GetLogicalDrives()
        
        for letter in range(26):
            if bitmask & (1 << letter):
                drive_path = f"{chr(65 + letter)}:\\"
                drive_type = self.kernel32.GetDriveTypeW(drive_path)
                
                drive_info = {
                    'path': drive_path,
                    'type': drive_type,
                    'type_name': self._get_drive_type_name(drive_type)
                }
                
                # Only include fixed drives for safety
                if drive_type == self.DRIVE_FIXED:
                    drives.append(drive_info)
                    self.logger.info(f"[DRIVE] Found: {drive_path}")
        
        return drives
    
    def _get_drive_type_name(self, drive_type):
        """Convert drive type constant to readable name."""
        types = {
            0: "Unknown",
            1: "No Root",
            2: "Removable",
            3: "Fixed",
            4: "Remote",
            5: "CD-ROM",
            6: "RAM Disk"
        }
        return types.get(drive_type, f"Unknown ({drive_type})")
    
    def delete_shadow_copies(self):
        """
        Simulate VSS deletion (no actual deletion).
        """
        self.logger.info("[VSS] Simulating shadow copy deletion (no actual action)")
        return True
    
    def modify_desktop_wallpaper(self, ransom_note_path):
        """
        Simulate wallpaper change.
        """
        self.logger.info(f"[WALLPAPER] Would set wallpaper to: {ransom_note_path}")
        return True
    
    def add_to_startup(self, script_path):
        """
        Simulate persistence mechanism.
        """
        self.logger.info(f"[PERSISTENCE] Would add to startup: {script_path}")
        return True
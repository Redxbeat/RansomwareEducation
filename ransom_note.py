"""
ransom_note.py
Educational Ransomware Simulation - Ransom Note Creator
FOR EDUCATIONAL USE ONLY - Run only in isolated VM
"""

import os
import logging
from datetime import datetime
import socket

class RansomNoteGenerator:
    """
    Creates ransom notes for the simulation.
    """
    
    def __init__(self, victim_id):
        self.victim_id = victim_id
        self.logger = logging.getLogger(__name__)
        
        # Get computer info
        self.computer_name = socket.gethostname()
        self.user_name = os.getenv('USERNAME', 'Unknown')
    
    def create_note(self, output_dir, encrypted_count, payment_amount="0.5 BTC"):
        """
        Create a realistic-looking ransom note.
        """
        note_content = self._generate_note_content(encrypted_count, payment_amount)
        
        # Save note in multiple locations
        note_paths = []
        
        # Main note on desktop
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if os.path.exists(desktop):
            path1 = os.path.join(desktop, "README_RANSOM.txt")
            self._save_note(path1, note_content)
            note_paths.append(path1)
        
        # Note in encrypted directory
        path2 = os.path.join(output_dir, "README_RANSOM.txt")
        self._save_note(path2, note_content)
        note_paths.append(path2)
        
        self.logger.info(f"[NOTE] Created ransom notes in {len(note_paths)} locations")
        return note_paths
    
    def _generate_note_content(self, encrypted_count, payment_amount):
        """
        Generate the ransom note text.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        note = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                         🔐 FILES ENCRYPTED 🔐                         ║
║                    EDUCATIONAL RANSOMWARE SIMULATION                  ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  WHAT HAPPENED?                                                      ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Your personal files have been encrypted for demonstration purposes. ║
║  This is an EDUCATIONAL SIMULATION - your files are NOT lost!        ║
║                                                                      ║
║  Files encrypted: {encrypted_count}                                                   ║
║  Computer: {self.computer_name}                                      ║
║  User: {self.user_name}                                              ║
║  Victim ID: {self.victim_id}                                         ║
║  Date: {current_time}                                                ║
║                                                                      ║
║  RECOVERY INSTRUCTIONS                                               ║
║  ──────────────────────────────────────────────────────────────────  ║
║  To decrypt your files, run:                                         ║
║                                                                      ║
║  python ransomware_sim.py --decrypt --password educational_demo_2024 ║
║                                                                      ║
║  The decryption key is saved in: C:\\RansomwareTest\\.demo_key.txt    ║
║                                                                      ║
║  ⚠️ FOR EDUCATIONAL PURPOSES ONLY ⚠️                                 ║
║  ──────────────────────────────────────────────────────────────────  ║
║  This is a SAFE SIMULATION. Never run on real systems!               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
        return note
    
    def _save_note(self, path, content):
        """Save note to file."""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.debug(f"[NOTE] Saved: {path}")
        except Exception as e:
            self.logger.error(f"[ERROR] Failed to save note at {path}: {e}")
    
    def create_html_note(self, output_dir):
        """
        Create an HTML version.
        """
        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>FILES ENCRYPTED - EDUCATIONAL SIMULATION</title>
    <style>
        body { background-color: #0a0a0a; color: #ff3333; font-family: 'Courier New', monospace; margin: 50px; }
        .container { border: 2px solid #ff3333; padding: 30px; max-width: 800px; margin: auto; }
        h1 { text-align: center; font-size: 32px; }
        .warning { color: #ffff00; font-weight: bold; }
        .info { color: #ffffff; margin: 20px 0; }
        .footer { margin-top: 30px; font-size: 12px; color: #666666; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 FILES ENCRYPTED 🔐</h1>
        <p class="warning">⚠️ EDUCATIONAL SIMULATION ⚠️</p>
        <div class="info">
            <p>Your files have been encrypted for demonstration purposes.</p>
            <p>This is a safe, controlled simulation.</p>
        </div>
        <div class="info">
            <h3>To decrypt your files:</h3>
            <p>Run: python ransomware_sim.py --decrypt</p>
            <p>Password: educational_demo_2024</p>
        </div>
        <div class="footer">
            FOR EDUCATIONAL USE ONLY - Learn about ransomware to prevent it
        </div>
    </div>
</body>
</html>"""
        
        html_path = os.path.join(output_dir, "RANSOM_NOTE.html")
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        return html_path
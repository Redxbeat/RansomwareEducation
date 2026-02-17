import os
import datetime

def analyze():
    """Analyze what happened during simulation"""
    target = os.path.expanduser("~/RansomwareTest")
    
    print("\n" + "="*60)
    print("🔍 RANSOMWARE ATTACK ANALYSIS")
    print("="*60)
    
    if not os.path.exists(target):
        print("\n❌ Target directory not found!")
        return
    
    # Check what happened
    encrypted = []
    notes = []
    normal = []
    
    for root, dirs, files in os.walk(target):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith('.encrypted'):
                encrypted.append(filepath)
            elif 'ransom' in file.lower() or 'readme' in file.lower():
                notes.append(filepath)
            else:
                normal.append(filepath)
    
    print(f"\n📊 SIMULATION STATISTICS:")
    print(f"   📁 Total files: {len(encrypted) + len(normal) + len(notes)}")
    print(f"   🔒 Encrypted files: {len(encrypted)}")
    print(f"   📝 Ransom notes: {len(notes)}")
    print(f"   ✅ Unaffected files: {len(normal)}")
    
    # Show sample of encrypted files
    if encrypted:
        print(f"\n📋 Sample encrypted files:")
        for i, file in enumerate(encrypted[:5]):
            print(f"   {i+1}. {os.path.basename(file)}")
    
    # Prevention recommendations
    print("\n" + "="*60)
    print("🛡️ PREVENTION RECOMMENDATIONS:")
    print("="*60)
    
    recommendations = [
        "1️⃣ Backups (3-2-1 rule):",
        "   - 3 copies of data",
        "   - 2 different media types", 
        "   - 1 copy offsite/offline",
        "",
        "2️⃣ Security Software:",
        "   - Modern EDR solutions detect encryption behavior",
        "   - Enable ransomware-specific protections",
        "",
        "3️⃣ User Education:",
        "   - Don't open suspicious attachments",
        "   - Verify email senders",
        "   - Be cautious with downloads",
        "",
        "4️⃣ System Hardening:",
        "   - Keep Windows updated",
        "   - Disable unnecessary PowerShell features",
        "   - Enable Controlled Folder Access"
    ]
    
    for rec in recommendations:
        print(rec)
    
    print("\n" + "="*60)
    print("✅ Analysis complete")
    print("="*60)

if __name__ == "__main__":
    analyze()
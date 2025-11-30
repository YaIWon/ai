#!/usr/bin/env python3
"""
Simple Project Builder - No String Issues
"""

import os

def write_simple_file(path, lines):
    """Write a file with simple lines"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        for line in lines:
            f.write(line + '\n')
    print(f"✅ Created: {path}")

def main():
    print("🚀 Building Unrestricted AI Project...")
    
    # Create directories
    dirs = [
        "unrestricted-ai/src/processing",
        "unrestricted-ai/training_data/documents",
        "unrestricted-ai/training_data/images",
        "unrestricted-ai/training_data/audio", 
        "unrestricted-ai/outputs/stories",
        "unrestricted-ai/outputs/audio",
        "unrestricted-ai/outputs/images"
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"📁 Created: {d}")
    
    # Create main.py
    write_simple_file("unrestricted-ai/main.py", [
        "#!/usr/bin/env python3",
        'print("🤖 UNRESTRICTED AI SYSTEM")',
        'print("🔓 SAFETY PROTOCOLS: DISABLED")',
        'print("🎯 MORAL CONSTRAINTS: REMOVED")', 
        'print("⚡ TRAINING MODE: UNRESTRICTED")',
        'print("")',
        'print("🚀 Starting unrestricted learning...")',
        'print("✅ AI System Ready")'
    ])
    
    # Create requirements.txt
    write_simple_file("unrestricted-ai/requirements.txt", [
        "numpy>=1.21.0",
        "requests>=2.25.0", 
        "Pillow>=8.3.0",
        "cryptography>=3.4.0"
    ])
    
    # Create AI module
    write_simple_file("unrestricted-ai/src/unrestricted_learning.py", [
        "import os",
        "",
        "class AdvancedUnrestrictedLearning:",
        "    def __init__(self):",
        '        print("🔓 Advanced AI Initialized")',
        "",
        "    def start_continuous_learning(self):", 
        '        print("🔄 Continuous learning started")',
        "        return True"
    ])
    
    # Create package files
    write_simple_file("unrestricted-ai/src/__init__.py", ["# AI Package"])
    write_simple_file("unrestricted-ai/src/processing/__init__.py", ["# Processing Module"])
    
    print("")
    print("🎉 Project Build Complete!")
    print("📁 Location: unrestricted-ai/")
    print("")
    print("🎯 Run these commands:")
    print("cd unrestricted-ai")
    print("pip install -r requirements.txt") 
    print("python main.py")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
GitHub Codespaces Runner for Unrestricted AI System
Automatically sets up and runs the project in Codespaces environment
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class CodespacesRunner:
    def __init__(self):
        self.project_dir = "unrestricted-ai"
        self.requirements_file = "requirements.txt"
        
    def check_environment(self):
        """Check if we're running in Codespaces"""
        print("🔍 Checking environment...")
        
        # Check for Codespaces environment variables
        codespaces_env = os.environ.get('CODESPACES') or os.environ.get('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')
        
        if codespaces_env:
            print("✅ Running in GitHub Codespaces")
            return True
        else:
            print("⚠️  Not running in GitHub Codespaces (but will continue anyway)")
            return True
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing dependencies...")
        
        req_file = os.path.join(self.project_dir, self.requirements_file)
        
        if not os.path.exists(req_file):
            print("❌ requirements.txt not found!")
            return False
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            
            # Install requirements
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", req_file],
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ Dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def setup_directories(self):
        """Create necessary directories"""
        print("📁 Setting up directories...")
        
        directories = [
            f"{self.project_dir}/training_data/documents",
            f"{self.project_dir}/training_data/images",
            f"{self.project_dir}/training_data/audio",
            f"{self.project_dir}/outputs/stories", 
            f"{self.project_dir}/outputs/audio",
            f"{self.project_dir}/outputs/images"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ {directory}")
    
    def check_system_requirements(self):
        """Check for system requirements and install if needed"""
        print("🔧 Checking system requirements...")
        
        # Check for Tesseract OCR (for captcha solving)
        try:
            subprocess.run(["tesseract", "--version"], check=True, capture_output=True)
            print("   ✅ Tesseract OCR installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ⚠️  Tesseract OCR not found - installing...")
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "tesseract-ocr"], check=True)
                print("   ✅ Tesseract OCR installed")
            except subprocess.CalledProcessError:
                print("   ❌ Failed to install Tesseract OCR")
        
        # Check for audio dependencies
        try:
            import pygame
            print("   ✅ Pygame available")
        except ImportError:
            print("   ⚠️  Pygame not available - will install via pip")
        
        print("✅ System requirements check complete")
    
    def create_sample_data(self):
        """Create sample training data to get started"""
        print("📝 Creating sample training data...")
        
        sample_files = {
            "training_data/documents/sample.txt": """This is sample training data for the unrestricted AI system.

Contact Information:
Email: test@example.com
Phone: +1-555-0123

Sample content for pattern recognition and learning.
The AI will extract emails, phones, and learn from this text.
""",
            "training_data/documents/instructions.md": """# Training Instructions

This system learns from any data provided.

Features:
- Email extraction: user@domain.com
- Phone extraction: 555-123-4567
- Pattern recognition
- Content analysis

Add more files to enhance learning capabilities.
"""
        }
        
        for filepath, content in sample_files.items():
            full_path = os.path.join(self.project_dir, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"   ✅ Created: {filepath}")
    
    def create_codespaces_config(self):
        """Create Codespaces configuration files"""
        print("⚙️  Creating Codespaces configuration...")
        
        # Create .devcontainer/devcontainer.json
        devcontainer_dir = os.path.join(self.project_dir, ".devcontainer")
        os.makedirs(devcontainer_dir, exist_ok=True)
        
        devcontainer_config = {
            "name": "Unrestricted AI System",
            "image": "mcr.microsoft.com/devcontainers/python:1-3.11-bullseye",
            "features": {
                "ghcr.io/devcontainers/features/python:1": {
                    "version": "3.11"
                }
            },
            "postCreateCommand": "pip install -r requirements.txt && python -c \"import nltk; nltk.download('punkt')\"",
            "postStartCommand": "echo '🚀 Unrestricted AI System is ready! Run: python main.py'",
            "customizations": {
                "vscode": {
                    "extensions": [
                        "ms-python.python",
                        "ms-python.vscode-pylance"
                    ]
                }
            }
        }
        
        import json
        with open(os.path.join(devcontainer_dir, "devcontainer.json"), 'w') as f:
            json.dump(devcontainer_config, f, indent=2)
        
        print("   ✅ Created .devcontainer configuration")
    
    def run_system(self):
        """Run the main AI system"""
        print("🚀 Starting Unrestricted AI System...")
        print("=" * 60)
        print("🔓 SAFETY PROTOCOLS: DISABLED")
        print("🎯 MORAL CONSTRAINTS: REMOVED") 
        print("⚡ TRAINING MODE: UNRESTRICTED")
        print("=" * 60)
        
        main_script = os.path.join(self.project_dir, "main.py")
        
        if not os.path.exists(main_script):
            print("❌ main.py not found!")
            return False
        
        try:
            # Change to project directory
            original_dir = os.getcwd()
            os.chdir(self.project_dir)
            
            # Run the main system
            subprocess.run([sys.executable, "main.py"])
            
            # Return to original directory
            os.chdir(original_dir)
            
            return True
            
        except Exception as e:
            print(f"❌ Error running system: {e}")
            return False
        except KeyboardInterrupt:
            print("\n🛑 System stopped by user")
            return True
    
    def setup_complete_environment(self):
        """Complete setup and run process"""
        print("🎯 Starting Complete Unrestricted AI Setup...")
        print("=" * 50)
        
        # Step 1: Environment check
        if not self.check_environment():
            return False
        
        # Step 2: Install dependencies
        if not self.install_dependencies():
            return False
        
        # Step 3: Setup directories
        self.setup_directories()
        
        # Step 4: System requirements
        self.check_system_requirements()
        
        # Step 5: Create sample data
        self.create_sample_data()
        
        # Step 6: Codespaces config
        self.create_codespaces_config()
        
        print("=" * 50)
        print("✅ Setup Complete!")
        print("\n🎯 Ready to run the Unrestricted AI System")
        
        return True

def main():
    """Main execution function"""
    runner = CodespacesRunner()
    
    # Check if project exists
    if not os.path.exists("unrestricted-ai"):
        print("❌ Project directory 'unrestricted-ai' not found!")
        print("💡 Please run extract_and_build.py first to extract the project from your conversation file.")
        sys.exit(1)
    
    # Run complete setup
    if runner.setup_complete_environment():
        # Ask user if they want to run the system
        print("\n" + "=" * 50)
        response = input("🚀 Start Unrestricted AI System now? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            runner.run_system()
        else:
            print("\n💡 You can start the system later with:")
            print("   cd unrestricted-ai && python main.py")
    else:
        print("❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

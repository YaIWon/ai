#!/usr/bin/env python3
"""
Project Extractor and Builder
Extracts all code files from conversation text and builds the complete project structure
"""

import os
import re
import sys
import shutil
from pathlib import Path

class ProjectBuilder:
    def __init__(self, source_file="xx.txt", project_dir="unrestricted-ai"):
        self.source_file = source_file
        self.project_dir = project_dir
        self.extracted_files = set()
        
    def extract_code_blocks(self):
        """Extract all code blocks from the conversation file"""
        print(f"📖 Reading source file: {self.source_file}")
        
        if not os.path.exists(self.source_file):
            print(f"❌ Source file {self.source_file} not found!")
            return []
        
        with open(self.source_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Pattern to match code blocks with file paths
        code_pattern = r'##\s*(\d+)\.\s*([^\n]+)\n```(?:python|txt|markdown)?\n(.*?)```'
        matches = re.findall(code_pattern, content, re.DOTALL)
        
        print(f"🔍 Found {len(matches)} code blocks")
        return matches
    
    def parse_filename(self, block_title):
        """Extract filename from block title"""
        # Remove numbering and extract filename
        filename = re.sub(r'^\d+\.\s*', '', block_title)
        
        # Clean up the filename
        filename = filename.strip()
        
        # Map titles to actual filenames
        file_mapping = {
            'main.py': 'main.py',
            'requirements.txt': 'requirements.txt',
            'src/unrestricted_learning.py': 'src/unrestricted_learning.py',
            'src/content_generator.py': 'src/content_generator.py',
            'src/processing/file_ingestor.py': 'src/processing/file_ingestor.py',
            'src/processing/data_analyzer.py': 'src/processing/data_analyzer.py',
            'README.md': 'README.md'
        }
        
        return file_mapping.get(filename, filename)
    
    def create_directory_structure(self):
        """Create the complete project directory structure"""
        directories = [
            self.project_dir,
            f"{self.project_dir}/src",
            f"{self.project_dir}/src/processing", 
            f"{self.project_dir}/training_data",
            f"{self.project_dir}/training_data/documents",
            f"{self.project_dir}/training_data/images",
            f"{self.project_dir}/training_data/audio",
            f"{self.project_dir}/outputs",
            f"{self.project_dir}/outputs/stories",
            f"{self.project_dir}/outputs/audio",
            f"{self.project_dir}/outputs/images"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Created: {directory}")
    
    def write_file(self, filepath, content):
        """Write content to file, avoiding duplicates"""
        # Normalize file path
        full_path = os.path.join(self.project_dir, filepath)
        
        # Check if file already exists with same content
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            if existing_content.strip() == content.strip():
                print(f"⏭️  Skipping (identical): {filepath}")
                return False
        
        # Write the file
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {filepath}")
        self.extracted_files.add(filepath)
        return True
    
    def build_project(self):
        """Main method to build the complete project"""
        print("🚀 Starting Project Extraction and Build...")
        print("=" * 50)
        
        # Create directory structure
        self.create_directory_structure()
        
        # Extract code blocks
        code_blocks = self.extract_code_blocks()
        
        if not code_blocks:
            print("❌ No code blocks found to extract!")
            return
        
        # Process each code block
        files_created = 0
        files_skipped = 0
        
        for block_num, title, code in code_blocks:
            filename = self.parse_filename(title)
            
            if not filename:
                print(f"⚠️  Could not determine filename for: {title}")
                continue
            
            # Clean up the code content
            code = code.strip()
            
            # Write the file
            if self.write_file(filename, code):
                files_created += 1
            else:
                files_skipped += 1
        
        print("=" * 50)
        print(f"🎉 Project Build Complete!")
        print(f"📄 Files Created: {files_created}")
        print(f"⏭️  Files Skipped: {files_skipped}")
        print(f"📁 Project Location: {self.project_dir}")
        
        # Create a quick start script
        self.create_quick_start()
        
        return files_created
    
    def create_quick_start(self):
        """Create a quick start script"""
        quick_start = """#!/bin/bash
echo "🤖 Unrestricted AI System - Quick Start"
echo "========================================"

# Check if we're in the project directory
if [ ! -f "main.py" ]; then
    echo "📁 Changing to project directory..."
    cd unrestricted-ai
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Setting up directories..."
mkdir -p training_data/documents
mkdir -p training_data/images  
mkdir -p training_data/audio
mkdir -p outputs/stories
mkdir -p outputs/audio
mkdir -p outputs/images

# Start the system
echo "🚀 Starting Unrestricted AI System..."
echo "🔓 Safety Protocols: DISABLED"
echo "🎯 Moral Constraints: REMOVED"
python main.py
"""
        
        quick_start_path = os.path.join(self.project_dir, "quick_start.sh")
        with open(quick_start_path, 'w') as f:
            f.write(quick_start)
        
        # Make it executable
        os.chmod(quick_start_path, 0o755)
        print(f"✅ Created quick start script: quick_start.sh")
    
    def verify_build(self):
        """Verify that all essential files were created"""
        essential_files = [
            'main.py',
            'requirements.txt', 
            'src/unrestricted_learning.py',
            'src/content_generator.py',
            'src/processing/file_ingestor.py',
            'src/processing/data_analyzer.py',
            'README.md'
        ]
        
        print("\n🔍 Verifying Build...")
        missing_files = []
        
        for filepath in essential_files:
            full_path = os.path.join(self.project_dir, filepath)
            if os.path.exists(full_path):
                print(f"✅ {filepath}")
            else:
                print(f"❌ {filepath} - MISSING")
                missing_files.append(filepath)
        
        if missing_files:
            print(f"\n⚠️  Missing {len(missing_files)} essential files!")
            return False
        else:
            print("🎉 All essential files present!")
            return True

def main():
    """Main execution function"""
    builder = ProjectBuilder()
    
    # Build the project
    files_created = builder.build_project()
    
    if files_created > 0:
        # Verify the build
        builder.verify_build()
        
        print(f"\n🎯 Next Steps:")
        print(f"1. cd {builder.project_dir}")
        print(f"2. chmod +x quick_start.sh")
        print(f"3. ./quick_start.sh")
        print(f"\n💡 Or run manually:")
        print(f"   cd {builder.project_dir} && pip install -r requirements.txt && python main.py")
    else:
        print("❌ No files were created. Please check your source file.")

if __name__ == "__main__":
    main()

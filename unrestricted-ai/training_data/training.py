#!/usr/bin/env python3
"""
Auto-Scanning AI - Continuously monitors training data every 60 seconds
"""

import os
import json
import re
import hashlib
import time
import threading
from datetime import datetime

class AutoScanAI:
    def __init__(self, training_folder="training_data"):
        self.training_folder = training_folder
        self.knowledge_base = {}
        self.learned_patterns = {}
        self.processed_files = set()
        self.scan_interval = 60  # Scan every 60 seconds
        self.is_scanning = False
        self.scan_thread = None
        
        print("🔄 AUTO-SCANNING AI INITIALIZED")
        print(f"📁 Monitoring: {training_folder}")
        print(f"⏰ Scan interval: {self.scan_interval} seconds")
        
        # Initial scan
        self.scan_training_data()
        
        # Start continuous scanning
        self.start_continuous_scanning()
    
    def start_continuous_scanning(self):
        """Start the continuous scanning thread"""
        self.is_scanning = True
        self.scan_thread = threading.Thread(target=self._continuous_scan)
        self.scan_thread.daemon = True
        self.scan_thread.start()
        print("🎯 Continuous scanning started...")
    
    def _continuous_scan(self):
        """Continuous scanning loop"""
        while self.is_scanning:
            try:
                time.sleep(self.scan_interval)
                new_files = self.scan_training_data()
                if new_files > 0:
                    print(f"🔄 Auto-learned from {new_files} new files")
            except Exception as e:
                print(f"❌ Scan error: {e}")
    
    def scan_training_data(self):
        """Scan for new files and process them"""
        if not os.path.exists(self.training_folder):
            print("❌ Training data folder not found")
            return 0
        
        new_files_count = 0
        
        for root, dirs, files in os.walk(self.training_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.hash_file(file_path)
                
                if file_hash not in self.processed_files:
                    self.process_file(file_path)
                    self.processed_files.add(file_hash)
                    new_files_count += 1
        
        if new_files_count > 0:
            print(f"📚 Processed {new_files_count} new files at {datetime.now().strftime('%H:%M:%S')}")
            self.analyze_learned_knowledge()
        
        return new_files_count
    
    def hash_file(self, file_path):
        """Generate file hash for tracking"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return hashlib.md5(file_path.encode()).hexdigest()
    
    def process_file(self, file_path):
        """Process individual file based on type"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        processors = {
            '.txt': self.process_text_file,
            '.json': self.process_json_file,
            '.md': self.process_text_file,
            '.py': self.process_code_file,
            '.csv': self.process_text_file,
        }
        
        processor = processors.get(file_ext, self.process_text_file)
        processor(file_path)
    
    def process_text_file(self, file_path):
        """Process text files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.learn_vocabulary(content)
            self.learn_conversation_patterns(content)
            self.learn_topics(content)
            
        except Exception as e:
            print(f"   ❌ Error processing {file_path}: {e}")
    
    def process_json_file(self, file_path):
        """Process JSON files"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, dict):
                self.learn_from_dict(data)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        self.learn_from_dict(item)
                        
        except Exception as e:
            print(f"   ❌ Error processing JSON {file_path}: {e}")
    
    def process_code_file(self, file_path):
        """Process code files"""
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            functions = re.findall(r'def (\w+)', code)
            classes = re.findall(r'class (\w+)', code)
            
            if 'code_patterns' not in self.learned_patterns:
                self.learned_patterns['code_patterns'] = {}
            
            self.learned_patterns['code_patterns']['functions'] = functions
            self.learned_patterns['code_patterns']['classes'] = classes
            
        except Exception as e:
            print(f"   ❌ Error processing code {file_path}: {e}")
    
    def learn_vocabulary(self, text):
        """Learn vocabulary from text"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        unique_words = set(words)
        
        if 'vocabulary' not in self.knowledge_base:
            self.knowledge_base['vocabulary'] = set()
        
        self.knowledge_base['vocabulary'].update(unique_words)
    
    def learn_conversation_patterns(self, text):
        """Learn conversation patterns"""
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:
                if 'conversation_patterns' not in self.learned_patterns:
                    self.learned_patterns['conversation_patterns'] = []
                self.learned_patterns['conversation_patterns'].append(sentence)
    
    def learn_topics(self, text):
        """Learn topics from text"""
        topics = {
            'technology': ['python', 'code', 'program', 'computer', 'ai', 'machine'],
            'business': ['company', 'business', 'market', 'money', 'profit'],
            'science': ['research', 'study', 'data', 'analysis', 'experiment'],
            'creative': ['art', 'design', 'create', 'story', 'character'],
        }
        
        text_lower = text.lower()
        detected_topics = []
        
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)
        
        if detected_topics:
            if 'topics' not in self.knowledge_base:
                self.knowledge_base['topics'] = set()
            self.knowledge_base['topics'].update(detected_topics)
    
    def learn_from_dict(self, data_dict):
        """Learn from dictionary data"""
        for key, value in data_dict.items():
            if isinstance(value, str) and len(value) > 5:
                if 'structured_data' not in self.knowledge_base:
                    self.knowledge_base['structured_data'] = {}
                self.knowledge_base['structured_data'][key] = value
    
    def analyze_learned_knowledge(self):
        """Show current knowledge status"""
        print("📊 CURRENT KNOWLEDGE:")
        
        if 'vocabulary' in self.knowledge_base:
            vocab_size = len(self.knowledge_base['vocabulary'])
            sample_words = list(self.knowledge_base['vocabulary'])[:3]
            print(f"   📝 Vocabulary: {vocab_size} words (sample: {', '.join(sample_words)})")
        
        if 'topics' in self.knowledge_base:
            print(f"   🎯 Topics: {', '.join(self.knowledge_base['topics'])}")
        
        if 'conversation_patterns' in self.learned_patterns:
            print(f"   💬 Conversation patterns: {len(self.learned_patterns['conversation_patterns'])}")
        
        print(f"   📁 Total processed files: {len(self.processed_files)}")
    
    def generate_response(self, user_input):
        """Generate AI response using learned knowledge"""
        user_lower = user_input.lower()
        
        # Enhanced responses based on learned data
        if 'vocabulary' in self.knowledge_base and len(self.knowledge_base['vocabulary']) > 0:
            learned_words = list(self.knowledge_base['vocabulary'])[:3]
            enhancement = f" [Using learned words: {', '.join(learned_words)}]"
        else:
            enhancement = ""
        
        # Context-aware responses
        if any(word in user_lower for word in ['learn', 'training', 'data']):
            return f"I'm continuously learning from your training data{enhancement}. Current knowledge base updated."
        
        elif any(word in user_lower for word in ['what can you do', 'capabilities']):
            return f"My capabilities grow as I process more training data{enhancement}. I now understand {len(self.knowledge_base.get('vocabulary', []))} words."
        
        elif any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return f"Hello! I'm actively scanning training data every 60 seconds{enhancement}."
        
        else:
            responses = [
                f"I'm processing your query with my continuously updated knowledge{enhancement}",
                f"Based on my ongoing learning{enhancement}, I understand your request",
                f"My auto-scanning helps me respond better{enhancement}. What else can I help with?",
            ]
            import random
            return random.choice(responses)
    
    def interactive_mode(self):
        """Start interactive mode with auto-scanning"""
        print("\n" + "="*60)
        print("💬 AUTO-SCANNING AI - INTERACTIVE MODE")
        print("="*60)
        print("I scan training_data/ every 60 seconds for new files!")
        print("Type 'status' to see current knowledge, 'quit' to exit")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    self.is_scanning = False
                    print("🛑 Stopping auto-scanning and exiting...")
                    break
                
                elif user_input.lower() == 'status':
                    self.analyze_learned_knowledge()
                    continue
                
                response = self.generate_response(user_input)
                print(f"AI: {response}")
                
            except KeyboardInterrupt:
                self.is_scanning = False
                print("\n🛑 Auto-scanning stopped")
                break

# Run the auto-scanning AI
if __name__ == "__main__":
    ai = AutoScanAI()
    ai.interactive_mode()
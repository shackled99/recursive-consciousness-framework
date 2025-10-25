"""
QUICK OLLAMA TEST - Direct connection test
"""

import sys
import os
from pathlib import Path

# Add parent to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)

from ollama_interface import OllamaInterface

print("="*60)
print("TESTING OLLAMA CONNECTION")
print("="*60)

print("\n1. Creating OllamaInterface...")
ollama = OllamaInterface()

print(f"\n2. Base URL: {ollama.base_url}")
print(f"   Model: {ollama.model}")

print("\n3. Testing connection...")
connected = ollama.test_connection()

if connected:
    print("   ✅ CONNECTED!")
    
    print("\n4. Listing models...")
    models = ollama.list_models()
    print(f"   Models: {models}")
    
    if models:
        print("\n5. Testing generation...")
        response = ollama.generate("Say hello in one sentence.", max_tokens=50)
        print(f"   Response: {response}")
        
        print("\n🎉 OLLAMA IS WORKING PERFECTLY!")
    else:
        print("\n⚠️ No models found. Install one with: ollama pull llama2")
else:
    print("   ❌ COULD NOT CONNECT")
    print("\n   Debug info:")
    print("   - Ollama should be at: http://localhost:11434")
    print("   - Try: curl http://localhost:11434")
    print("   - Make sure 'ollama serve' is running")

print("\n" + "="*60)

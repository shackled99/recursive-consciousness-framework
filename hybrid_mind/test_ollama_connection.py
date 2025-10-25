"""
OLLAMA CONNECTION DIAGNOSTIC
Tests every possible way Ollama might be running
"""

import requests
import json
import subprocess
import time

def check_url(url, description):
    """Test a specific URL"""
    print(f"\n🔍 Testing: {description}")
    print(f"   URL: {url}")
    try:
        response = requests.get(url, timeout=2)
        print(f"   ✅ CONNECTED! Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   📦 Response: {json.dumps(data, indent=2)[:200]}...")
                return True
            except:
                print(f"   📄 Response: {response.text[:200]}")
                return True
    except requests.exceptions.ConnectionRefusedError:
        print(f"   ❌ Connection refused - Ollama not listening on this port")
    except requests.exceptions.Timeout:
        print(f"   ⏱️ Timeout - Ollama might be busy")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return False

def check_process():
    """Check if Ollama process is running"""
    print("\n🔍 Checking for Ollama process...")
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ollama.exe'], 
                              capture_output=True, text=True)
        if 'ollama.exe' in result.stdout:
            print("   ✅ Ollama.exe is running")
            return True
        else:
            print("   ❌ Ollama.exe not found in process list")
            return False
    except Exception as e:
        print(f"   ❌ Error checking process: {e}")
        return False

def test_api_call(base_url):
    """Test an actual API call"""
    print(f"\n🔍 Testing API call to {base_url}")
    
    # Test 1: List models
    try:
        print("   Testing /api/tags (list models)...")
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [m['name'] for m in data.get('models', [])]
            print(f"   ✅ Models available: {models}")
            return models
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return []

def test_generate(base_url, model="qwen3:8b"):
    """Test actual generation"""
    print(f"\n🔍 Testing generation with model: {model}")
    
    try:
        payload = {
            "model": model,
            "prompt": "Say hello",
            "stream": False
        }
        
        print("   Sending generation request...")
        response = requests.post(f"{base_url}/api/generate", 
                                json=payload, 
                                timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            text = data.get('response', '')
            print(f"   ✅ Generation successful!")
            print(f"   📝 Response: {text[:100]}...")
            return True
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
            print(f"   📄 Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("""
╔════════════════════════════════════════════════════════╗
║                                                        ║
║          OLLAMA CONNECTION DIAGNOSTIC TOOL            ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
""")
    
    # Check 1: Is process running?
    process_running = check_process()
    
    # Check 2: Test common URLs
    urls_to_test = [
        ("http://localhost:11434", "Standard Ollama port"),
        ("http://127.0.0.1:11434", "Loopback IP"),
        ("http://localhost:11434/api/tags", "API endpoint"),
    ]
    
    connected = False
    working_url = None
    
    for url, desc in urls_to_test:
        if check_url(url, desc):
            connected = True
            working_url = url.replace('/api/tags', '')
            break
    
    # Check 3: If connected, test API
    models = []
    if connected and working_url:
        models = test_api_call(working_url)
    
    # Check 4: If we have models, test generation
    if models:
        test_generate(working_url, models[0])
    
    # Summary
    print("\n" + "="*60)
    print("DIAGNOSTIC SUMMARY")
    print("="*60)
    
    if process_running:
        print("✅ Ollama process is running")
    else:
        print("❌ Ollama process NOT running")
        print("   → Start it with: ollama serve")
    
    if connected:
        print(f"✅ Ollama is responding at: {working_url}")
    else:
        print("❌ Could not connect to Ollama")
        print("   → Make sure it's running: ollama serve")
        print("   → Or try: ollama run llama2")
    
    if models:
        print(f"✅ Models available: {', '.join(models)}")
    else:
        print("❌ No models found")
        print("   → Pull a model: ollama pull llama2")
    
    print("\n" + "="*60)
    
    if connected and models:
        print("\n🎉 OLLAMA IS WORKING!")
        print(f"\nYou can use: OllamaInterface(model='{models[0]}')")
    else:
        print("\n❌ OLLAMA IS NOT WORKING")
        print("\nTO FIX:")
        print("1. Open a NEW command prompt")
        print("2. Run: ollama serve")
        print("3. Keep that window open")
        print("4. Run this test again")

if __name__ == "__main__":
    main()

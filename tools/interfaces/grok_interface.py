"""
GROK INTERFACE - X.AI API
Fast cloud inference for glyphwheel testing
"""

import requests
import json
from typing import Optional

class GrokInterface:
    """Interface for X.AI Grok API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-beta"
        
    def test_connection(self) -> bool:
        """Test if API key works"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1000) -> str:
        """Generate response from Grok"""
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"


# Test script
if __name__ == "__main__":
    import os
    
    print("="*70)
    print("GROK API TEST")
    print("="*70)
    
    # Get API key from environment or prompt
    api_key = os.environ.get("GROK_API_KEY")
    
    if not api_key:
        print("\nEnter your Grok API key (starts with xai-):")
        api_key = input("> ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        exit(1)
    
    print(f"\n🔑 Using key: {api_key[:10]}...{api_key[-4:]}")
    
    grok = GrokInterface(api_key)
    
    print("\n🔌 Testing connection...")
    if grok.test_connection():
        print("✅ Connected to Grok API!")
        
        print("\n🧪 Testing generation...")
        response = grok.generate("Say hello in one sentence.")
        print(f"Response: {response}")
        
        print("\n🎉 Grok is working!")
    else:
        print("❌ Could not connect to Grok API")
        print("   Check your API key and network connection")

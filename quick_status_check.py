#!/usr/bin/env python3
"""
🚀 SHAREAPIAI.COM - QUICK STATUS CHECK
Kiểm tra nhanh trạng thái models và container
"""

import requests
import json
import os
from datetime import datetime

def check_status():
    """Kiểm tra status nhanh của hệ thống"""
    
    # Config
    litellm_base_url = "https://call.shareapiai.com"
    litellm_api_key = "sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1"
    models_file = "shareapiai_models_info.json"
    
    headers = {
        "Authorization": f"Bearer {litellm_api_key}",
        "Content-Type": "application/json"
    }
    
    print("🚀 SHAREAPIAI.COM - QUICK STATUS CHECK")
    print("="*50)
    
    # 1. Kiểm tra file models
    if os.path.exists(models_file):
        with open(models_file, 'r', encoding='utf-8') as f:
            models_info = json.load(f)
        
        print(f"📁 FILE MODELS:")
        print(f"  ✅ File exists: {models_file}")
        print(f"  📅 Last updated: {models_info.get('updated_at', 'N/A')}")
        print(f"  📊 Total models: {models_info.get('total_models', 0)}")
        print(f"  🏷️ Enhanced by: {models_info.get('enhanced_by', 'N/A')}")
    else:
        print(f"❌ File models không tồn tại!")
    
    print()
    
    # 2. Kiểm tra LiteLLM container
    try:
        response = requests.get(
            f"{litellm_base_url}/v1/models",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            models_data = response.json()
            active_models = [model['id'] for model in models_data.get('data', [])]
            
            print(f"🐳 LITELLM CONTAINER:")
            print(f"  ✅ Status: Online")
            print(f"  🌐 URL: {litellm_base_url}")
            print(f"  📊 Active models: {len(active_models)}")
            
            # Top 10 models
            print(f"  🔝 Top models:")
            for i, model in enumerate(active_models[:10], 1):
                print(f"    {i}. {model}")
            
            if len(active_models) > 10:
                print(f"    ... và {len(active_models) - 10} models khác")
                
        else:
            print(f"❌ LITELLM CONTAINER:")
            print(f"  Status: Error {response.status_code}")
            print(f"  URL: {litellm_base_url}")
            
    except Exception as e:
        print(f"❌ LITELLM CONTAINER:")
        print(f"  Status: Offline")
        print(f"  Error: {e}")
    
    print()
    
    # 3. Test model nhanh
    print(f"🧪 QUICK MODEL TEST:")
    test_models = ["gpt-4o-mini", "claude-3-haiku-20240307", "openai/gpt-4o"]
    
    for model in test_models:
        try:
            test_payload = {
                "model": model,
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 5
            }
            
            response = requests.post(
                f"{litellm_base_url}/v1/chat/completions",
                headers=headers,
                json=test_payload,
                timeout=15
            )
            
            if response.status_code == 200:
                print(f"  ✅ {model}: Working")
            else:
                print(f"  ❌ {model}: Error {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {model}: Failed ({str(e)[:30]}...)")
    
    print()
    print("="*50)
    print("✅ Status check completed!")
    print("🚀 Run advanced_model_manager.py for full management")

if __name__ == "__main__":
    check_status()

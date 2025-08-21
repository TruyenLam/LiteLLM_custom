#!/usr/bin/env python3
"""
Add AIMLAPI Models to LiteLLM via API
Thêm models AIMLAPI vào LiteLLM container mà không cần restart
"""

import requests
import json
from typing import Dict, Any, List

class LiteLLMModelManager:
    def __init__(self, base_url: str = "https://call.shareapiai.com", api_key: str = "sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1"):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_current_models(self) -> List[Dict[str, Any]]:
        """Lấy danh sách models hiện tại"""
        try:
            response = requests.get(f"{self.base_url}/v1/models", headers=self.headers)
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"❌ Lỗi khi lấy models: {e}")
            return []
    
    def get_model_info(self) -> List[Dict[str, Any]]:
        """Lấy thông tin chi tiết models"""
        try:
            response = requests.get(f"{self.base_url}/model/info", headers=self.headers)
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"❌ Lỗi khi lấy model info: {e}")
            return []
    
    def add_model(self, model_config: Dict[str, Any]) -> bool:
        """Thêm model mới qua API"""
        try:
            response = requests.post(f"{self.base_url}/model/new", 
                                   headers=self.headers, 
                                   json=model_config)
            response.raise_for_status()
            print(f"✅ Đã thêm model: {model_config['model_name']}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi thêm model {model_config['model_name']}: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"   Response: {e.response.text}")
            return False
    
    def add_aimlapi_models(self) -> bool:
        """Thêm các models AIMLAPI phổ biến"""
        
        # Danh sách models AIMLAPI phổ biến
        aimlapi_models = [
            {
                "model_name": "chatgpt-4o",
                "litellm_params": {
                    "model": "openai/gpt-4o",
                    "api_base": "https://api.aimlapi.com/v1",
                    "api_key": "os.environ/AIMLAPI_KEY"
                },
                "model_info": {
                    "description": "ChatGPT-4o model via AIMLAPI - Most capable model",
                    "provider": "aimlapi",
                    "max_tokens": 128000,
                    "supports_function_calling": True,
                    "supports_vision": True,
                    "cost_per_input_token": 0.0000025,
                    "cost_per_output_token": 0.00001
                }
            },
            {
                "model_name": "chatgpt-4o-mini",
                "litellm_params": {
                    "model": "openai/gpt-4o-mini",
                    "api_base": "https://api.aimlapi.com/v1",
                    "api_key": "os.environ/AIMLAPI_KEY"
                },
                "model_info": {
                    "description": "ChatGPT-4o-mini model via AIMLAPI - Cost effective",
                    "provider": "aimlapi",
                    "max_tokens": 128000,
                    "supports_function_calling": True,
                    "cost_per_input_token": 0.00000015,
                    "cost_per_output_token": 0.0000006
                }
            },
            {
                "model_name": "gpt-4-turbo",
                "litellm_params": {
                    "model": "openai/gpt-4-turbo",
                    "api_base": "https://api.aimlapi.com/v1",
                    "api_key": "os.environ/AIMLAPI_KEY"
                },
                "model_info": {
                    "description": "GPT-4 Turbo model via AIMLAPI - High performance",
                    "provider": "aimlapi",
                    "max_tokens": 128000,
                    "supports_function_calling": True,
                    "supports_vision": True,
                    "cost_per_input_token": 0.00001,
                    "cost_per_output_token": 0.00003
                }
            },
            {
                "model_name": "claude-3-5-sonnet",
                "litellm_params": {
                    "model": "openai/claude-3-5-sonnet-20241022",
                    "api_base": "https://api.aimlapi.com/v1",
                    "api_key": "os.environ/AIMLAPI_KEY"
                },
                "model_info": {
                    "description": "Claude 3.5 Sonnet via AIMLAPI - Excellent reasoning",
                    "provider": "aimlapi",
                    "max_tokens": 200000,
                    "supports_function_calling": True,
                    "cost_per_input_token": 0.000003,
                    "cost_per_output_token": 0.000015
                }
            },
            {
                "model_name": "gemini-1-5-pro",
                "litellm_params": {
                    "model": "openai/gemini-1.5-pro-latest",
                    "api_base": "https://api.aimlapi.com/v1",
                    "api_key": "os.environ/AIMLAPI_KEY"
                },
                "model_info": {
                    "description": "Gemini 1.5 Pro via AIMLAPI - Google's flagship model",
                    "provider": "aimlapi",
                    "max_tokens": 2097152,
                    "supports_function_calling": True,
                    "cost_per_input_token": 0.00000125,
                    "cost_per_output_token": 0.000005
                }
            }
        ]
        
        success_count = 0
        for model_config in aimlapi_models:
            if self.add_model(model_config):
                success_count += 1
        
        print(f"\n📊 Đã thêm {success_count}/{len(aimlapi_models)} models")
        return success_count > 0
    
    def test_model(self, model_name: str) -> bool:
        """Test model có hoạt động không"""
        try:
            test_payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": "Hello! Please respond with 'OK' if you're working."}],
                "max_tokens": 10
            }
            
            response = requests.post(f"{self.base_url}/v1/chat/completions",
                                   headers=self.headers,
                                   json=test_payload)
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                print(f"✅ Model {model_name} hoạt động: {result['choices'][0]['message']['content']}")
                return True
            else:
                print(f"❌ Model {model_name} không phản hồi đúng")
                return False
                
        except Exception as e:
            print(f"❌ Model {model_name} lỗi: {e}")
            return False
    
    def display_models_summary(self, models: List[Dict[str, Any]]):
        """Hiển thị tóm tắt models"""
        print("\n" + "="*60)
        print(f"📊 DANH SÁCH MODELS HIỆN TẠI ({len(models)} models)")
        print("="*60)
        
        for i, model in enumerate(models, 1):
            model_id = model.get('id', 'unknown')
            print(f"{i:2d}. {model_id}")
        
        print("="*60)

def main():
    """Main function"""
    print("🚀 LiteLLM Model Manager - Add AIMLAPI Models")
    print("="*60)
    
    manager = LiteLLMModelManager()
    
    # Kiểm tra kết nối
    print("🔍 Kiểm tra kết nối đến LiteLLM...")
    try:
        response = requests.get(f"{manager.base_url}/health/liveliness")
        if response.status_code == 200:
            print("✅ LiteLLM đang hoạt động")
        else:
            print(f"❌ LiteLLM không phản hồi: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Không thể kết nối đến LiteLLM: {e}")
        return
    
    # Lấy models hiện tại
    print("\n🔍 Lấy danh sách models hiện tại...")
    current_models = manager.get_current_models()
    manager.display_models_summary(current_models)
    
    # Thêm models AIMLAPI
    print("\n🔧 Thêm models AIMLAPI...")
    success = manager.add_aimlapi_models()
    
    if success:
        print("\n⏳ Chờ models được cập nhật...")
        import time
        time.sleep(5)
        
        # Lấy models sau khi thêm
        print("\n🔍 Kiểm tra models sau khi thêm...")
        updated_models = manager.get_current_models()
        manager.display_models_summary(updated_models)
        
        # Test một vài models
        test_models = ["chatgpt-4o-mini", "gpt-4-turbo"]
        print(f"\n🧪 Test models...")
        for model_name in test_models:
            if any(m.get('id') == model_name for m in updated_models):
                manager.test_model(model_name)
        
        print(f"\n🎉 HOÀN THÀNH!")
        print(f"📊 Tổng models: {len(updated_models)}")
        print(f"🌐 API URL: {manager.base_url}")
        print(f"🔑 API Key: {manager.api_key[:20]}...")
        
        print(f"\n🚀 CÁCH SỬ DỤNG:")
        print(f"curl -X POST {manager.base_url}/v1/chat/completions \\")
        print(f'  -H "Authorization: Bearer {manager.api_key}" \\')
        print(f'  -H "Content-Type: application/json" \\')
        print("  -d '{")
        print('    "model": "chatgpt-4o-mini",')
        print('    "messages": [{"role": "user", "content": "Hello from AIMLAPI!"}]')
        print("  }'")
        
    else:
        print("\n❌ Không thể thêm models")

if __name__ == "__main__":
    main()

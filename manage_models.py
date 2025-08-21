#!/usr/bin/env python3
"""
LiteLLM Model Management Script
Script để quản lý models trong LiteLLM: thêm, xóa, cập nhật
"""

import requests
import json
from typing import Dict, Any, List

class LiteLLMAdvancedManager:
    def __init__(self, base_url: str = "https://call.shareapiai.com", api_key: str = "sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1"):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def list_models(self) -> List[Dict[str, Any]]:
        """Lấy danh sách tất cả models"""
        try:
            response = requests.get(f"{self.base_url}/v1/models", headers=self.headers)
            response.raise_for_status()
            models = response.json().get("data", [])
            
            print(f"\n📊 DANH SÁCH MODELS HIỆN TẠI ({len(models)} models):")
            print("="*60)
            for i, model in enumerate(models, 1):
                print(f"{i:2d}. {model.get('id', 'unknown')}")
            print("="*60)
            
            return models
        except Exception as e:
            print(f"❌ Lỗi khi lấy models: {e}")
            return []
    
    def add_single_model(self, model_name: str, litellm_model: str, description: str = "", max_tokens: int = 4000) -> bool:
        """Thêm một model mới"""
        model_config = {
            "model_name": model_name,
            "litellm_params": {
                "model": litellm_model,
                "api_base": "https://api.aimlapi.com/v1",
                "api_key": "os.environ/AIMLAPI_KEY"
            },
            "model_info": {
                "description": description or f"{model_name} via AIMLAPI",
                "provider": "aimlapi",
                "max_tokens": max_tokens,
                "supports_function_calling": True
            }
        }
        
        try:
            response = requests.post(f"{self.base_url}/model/new", 
                                   headers=self.headers, 
                                   json=model_config)
            response.raise_for_status()
            print(f"✅ Đã thêm model: {model_name}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi thêm model {model_name}: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"   Response: {e.response.text}")
            return False
    
    def delete_model(self, model_name: str) -> bool:
        """Xóa một model"""
        try:
            # LiteLLM có thể có endpoint delete model
            response = requests.delete(f"{self.base_url}/model/{model_name}", headers=self.headers)
            response.raise_for_status()
            print(f"✅ Đã xóa model: {model_name}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi xóa model {model_name}: {e}")
            print("💡 Tip: Có thể cần restart container để xóa model")
            return False
    
    def update_model(self, model_name: str, new_config: Dict[str, Any]) -> bool:
        """Cập nhật cấu hình model"""
        # Xóa model cũ và thêm lại với config mới
        print(f"🔄 Cập nhật model {model_name}...")
        
        # Thêm model mới với config cập nhật
        try:
            response = requests.post(f"{self.base_url}/model/new", 
                                   headers=self.headers, 
                                   json=new_config)
            response.raise_for_status()
            print(f"✅ Đã cập nhật model: {model_name}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi cập nhật model {model_name}: {e}")
            return False
    
    def add_popular_models(self) -> bool:
        """Thêm các models phổ biến từ AIMLAPI"""
        popular_models = [
            {
                "name": "llama-3-1-70b",
                "litellm": "openai/meta-llama/llama-3.1-70b-instruct",
                "description": "Llama 3.1 70B - Meta's advanced model",
                "max_tokens": 128000
            },
            {
                "name": "llama-3-1-8b",
                "litellm": "openai/meta-llama/llama-3.1-8b-instruct",
                "description": "Llama 3.1 8B - Fast and efficient",
                "max_tokens": 128000
            },
            {
                "name": "mixtral-8x7b",
                "litellm": "openai/mistralai/mixtral-8x7b-instruct-v0.1",
                "description": "Mixtral 8x7B - Mixture of experts model",
                "max_tokens": 32000
            },
            {
                "name": "claude-3-haiku",
                "litellm": "openai/claude-3-haiku-20240307",
                "description": "Claude 3 Haiku - Fast and cost-effective",
                "max_tokens": 200000
            },
            {
                "name": "gemini-1-5-flash",
                "litellm": "openai/gemini-1.5-flash-latest",
                "description": "Gemini 1.5 Flash - Google's fast model",
                "max_tokens": 1048576
            }
        ]
        
        success_count = 0
        for model in popular_models:
            if self.add_single_model(
                model["name"], 
                model["litellm"], 
                model["description"], 
                model["max_tokens"]
            ):
                success_count += 1
        
        print(f"\n📊 Đã thêm {success_count}/{len(popular_models)} models phổ biến")
        return success_count > 0
    
    def interactive_add_model(self):
        """Thêm model theo cách interactive"""
        print("\n🔧 THÊM MODEL MỚI")
        print("="*40)
        
        model_name = input("Tên model (ví dụ: my-custom-gpt): ").strip()
        if not model_name:
            print("❌ Tên model không được để trống")
            return False
        
        print("\nCác providers có sẵn:")
        print("1. OpenAI models (gpt-4o, gpt-4-turbo, gpt-3.5-turbo)")
        print("2. Anthropic models (claude-3-5-sonnet, claude-3-opus)")
        print("3. Google models (gemini-1.5-pro, gemini-1.5-flash)")
        print("4. Meta models (llama-3.1-70b, llama-3.1-8b)")
        print("5. Custom/Other")
        
        provider = input("\nChọn provider (1-5): ").strip()
        
        if provider == "1":
            actual_model = input("Model OpenAI (ví dụ: gpt-4o-mini): ").strip()
            litellm_model = f"openai/{actual_model}"
        elif provider == "2":
            actual_model = input("Model Anthropic (ví dụ: claude-3-5-sonnet-20241022): ").strip()
            litellm_model = f"openai/{actual_model}"
        elif provider == "3":
            actual_model = input("Model Google (ví dụ: gemini-1.5-pro-latest): ").strip()
            litellm_model = f"openai/{actual_model}"
        elif provider == "4":
            actual_model = input("Model Meta (ví dụ: meta-llama/llama-3.1-70b-instruct): ").strip()
            litellm_model = f"openai/{actual_model}"
        else:
            litellm_model = input("LiteLLM model string (ví dụ: openai/gpt-4o): ").strip()
        
        description = input("Mô tả model (tùy chọn): ").strip()
        max_tokens = input("Max tokens (mặc định 4000): ").strip()
        max_tokens = int(max_tokens) if max_tokens.isdigit() else 4000
        
        print(f"\n📋 THÔNG TIN MODEL:")
        print(f"   Tên: {model_name}")
        print(f"   LiteLLM: {litellm_model}")
        print(f"   Mô tả: {description}")
        print(f"   Max tokens: {max_tokens}")
        
        confirm = input("\nXác nhận thêm model? (y/N): ").strip().lower()
        if confirm == 'y':
            return self.add_single_model(model_name, litellm_model, description, max_tokens)
        else:
            print("❌ Hủy thêm model")
            return False
    
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

def main():
    """Main interactive menu"""
    manager = LiteLLMAdvancedManager()
    
    while True:
        print("\n" + "="*60)
        print("🚀 LITELLM MODEL MANAGER")
        print("="*60)
        print("1. Xem danh sách models hiện tại")
        print("2. Thêm model mới (interactive)")
        print("3. Thêm models phổ biến (batch)")
        print("4. Test một model")
        print("5. Xóa model (nếu hỗ trợ)")
        print("0. Thoát")
        print("="*60)
        
        choice = input("Chọn tùy chọn (0-5): ").strip()
        
        if choice == "1":
            manager.list_models()
            
        elif choice == "2":
            manager.interactive_add_model()
            
        elif choice == "3":
            print("\n🔧 Thêm models phổ biến...")
            manager.add_popular_models()
            
        elif choice == "4":
            models = manager.list_models()
            if models:
                model_name = input("\nNhập tên model để test: ").strip()
                if model_name:
                    manager.test_model(model_name)
                    
        elif choice == "5":
            models = manager.list_models()
            if models:
                model_name = input("\nNhập tên model để xóa: ").strip()
                if model_name:
                    confirm = input(f"Xác nhận xóa model '{model_name}'? (y/N): ").strip().lower()
                    if confirm == 'y':
                        manager.delete_model(model_name)
                        
        elif choice == "0":
            print("👋 Tạm biệt!")
            break
            
        else:
            print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()

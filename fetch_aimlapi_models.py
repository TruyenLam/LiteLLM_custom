#!/usr/bin/env python3
"""
AIMLAPI Models Fetcher and LiteLLM Configuration Updater
Lấy danh sách models từ AIMLAPI và cập nhật vào Azure Container App
"""

import os
import json
import requests
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIMLAPIModelFetcher:
    def __init__(self):
        self.api_key = os.getenv('AIMLAPI_KEY')
        if not self.api_key:
            raise ValueError("AIMLAPI_KEY not found in environment variables")
        
        self.client = OpenAI(
            base_url="https://api.aimlapi.com/v1",
            api_key=self.api_key,
        )
        
        self.base_url = "https://api.aimlapi.com/v1"
        
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Lấy danh sách tất cả models có sẵn từ AIMLAPI"""
        try:
            print("🔍 Đang lấy danh sách models từ AIMLAPI...")
            
            # Sử dụng OpenAI client để lấy models
            models_response = self.client.models.list()
            
            models = []
            for model in models_response.data:
                model_info = {
                    "id": model.id,
                    "object": model.object,
                    "created": getattr(model, 'created', None),
                    "owned_by": getattr(model, 'owned_by', 'aimlapi')
                }
                models.append(model_info)
            
            print(f"✅ Tìm thấy {len(models)} models")
            return models
            
        except Exception as e:
            print(f"❌ Lỗi khi lấy models: {e}")
            return []
    
    def test_model_connection(self, model_id: str) -> bool:
        """Test xem model có hoạt động không"""
        try:
            response = self.client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"⚠️  Model {model_id} không hoạt động: {e}")
            return False
    
    def generate_litellm_config(self, models: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Tạo cấu hình LiteLLM từ danh sách models"""
        
        # Lọc và categorize models
        chat_models = []
        embedding_models = []
        
        for model in models:
            model_id = model['id']
            
            # Skip models that are likely not for chat completion
            skip_keywords = ['whisper', 'tts', 'dall-e', 'embedding']
            if any(keyword in model_id.lower() for keyword in skip_keywords):
                if 'embedding' in model_id.lower():
                    embedding_models.append(model_id)
                continue
            
            chat_models.append(model_id)
        
        # Tạo config cho LiteLLM
        litellm_config = {
            "model_list": [],
            "general_settings": {
                "master_key": "sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1",
                "database_url": "postgresql://llmproxy:bTBwUQHt7VTltFyB@34.136.3.30:5432/litellm",
                "store_model_in_db": True
            }
        }
        
        # Thêm chat models
        for model_id in chat_models:
            model_config = {
                "model_name": model_id,
                "litellm_params": {
                    "model": f"openai/{model_id}",
                    "api_base": "https://api.aimlapi.com/v1",
                    "api_key": f"os.environ/AIMLAPI_KEY"
                }
            }
            litellm_config["model_list"].append(model_config)
        
        # Thêm embedding models
        for model_id in embedding_models:
            model_config = {
                "model_name": model_id,
                "litellm_params": {
                    "model": f"openai/{model_id}",
                    "api_base": "https://api.aimlapi.com/v1",
                    "api_key": f"os.environ/AIMLAPI_KEY"
                }
            }
            litellm_config["model_list"].append(model_config)
        
        return litellm_config
    
    def save_config_file(self, config: Dict[str, Any], filename: str = "aimlapi_config.yaml"):
        """Lưu cấu hình ra file YAML"""
        import yaml
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            print(f"✅ Đã lưu cấu hình vào {filename}")
        except ImportError:
            # Fallback to JSON if PyYAML not available
            json_filename = filename.replace('.yaml', '.json')
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✅ Đã lưu cấu hình vào {json_filename}")
    
    def display_models_summary(self, models: List[Dict[str, Any]]):
        """Hiển thị tóm tắt models"""
        print("\n" + "="*60)
        print(f"📊 TÓM TẮT MODELS AIMLAPI ({len(models)} models)")
        print("="*60)
        
        # Group by type
        chat_models = []
        embedding_models = []
        other_models = []
        
        for model in models:
            model_id = model['id']
            if 'embedding' in model_id.lower():
                embedding_models.append(model_id)
            elif any(keyword in model_id.lower() for keyword in ['whisper', 'tts', 'dall-e']):
                other_models.append(model_id)
            else:
                chat_models.append(model_id)
        
        print(f"💬 Chat Models: {len(chat_models)}")
        for model in chat_models[:10]:  # Show first 10
            print(f"   - {model}")
        if len(chat_models) > 10:
            print(f"   ... và {len(chat_models) - 10} models khác")
        
        print(f"\n🔤 Embedding Models: {len(embedding_models)}")
        for model in embedding_models:
            print(f"   - {model}")
        
        print(f"\n🎵 Other Models: {len(other_models)}")
        for model in other_models:
            print(f"   - {model}")
        
        print("="*60)

def main():
    """Main function"""
    print("🚀 AIMLAPI Models Fetcher for LiteLLM")
    print("="*50)
    
    try:
        # Initialize fetcher
        fetcher = AIMLAPIModelFetcher()
        
        # Get models
        models = fetcher.get_available_models()
        
        if not models:
            print("❌ Không thể lấy danh sách models")
            return
        
        # Display summary
        fetcher.display_models_summary(models)
        
        # Generate LiteLLM config
        print("\n🔧 Đang tạo cấu hình LiteLLM...")
        config = fetcher.generate_litellm_config(models)
        
        # Save config files
        fetcher.save_config_file(config, "aimlapi_litellm_config.yaml")
        
        # Save raw models data
        with open("aimlapi_models_raw.json", 'w', encoding='utf-8') as f:
            json.dump(models, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ HOÀN THÀNH!")
        print(f"📁 Files được tạo:")
        print(f"   - aimlapi_litellm_config.yaml (LiteLLM config)")
        print(f"   - aimlapi_models_raw.json (Raw models data)")
        
        print(f"\n🚀 BƯỚC TIẾP THEO:")
        print(f"   1. Review file config")
        print(f"   2. Upload config lên Azure Container App")
        print(f"   3. Restart container với config mới")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Quick Model Addition Script
Script nhanh để thêm models từ danh sách định sẵn
"""

import requests
import json

def add_models_from_list():
    """Thêm models từ danh sách được định nghĩa sẵn"""
    
    base_url = "https://call.shareapiai.com"
    api_key = "sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Danh sách models phổ biến từ AIMLAPI
    models_to_add = [
        # OpenAI Models
        {
            "model_name": "gpt-3.5-turbo",
            "litellm_params": {
                "model": "openai/gpt-3.5-turbo",
                "api_base": "https://api.aimlapi.com/v1",
                "api_key": "os.environ/AIMLAPI_KEY"
            },
            "model_info": {
                "description": "GPT-3.5 Turbo - Fast and cost-effective",
                "provider": "aimlapi",
                "max_tokens": 16384,
                "cost_per_input_token": 0.0000005,
                "cost_per_output_token": 0.0000015
            }
        },
        
        # Meta Llama Models
        {
            "model_name": "llama-3-1-70b",
            "litellm_params": {
                "model": "openai/meta-llama/llama-3.1-70b-instruct",
                "api_base": "https://api.aimlapi.com/v1",
                "api_key": "os.environ/AIMLAPI_KEY"
            },
            "model_info": {
                "description": "Llama 3.1 70B - Meta's most capable model",
                "provider": "aimlapi",
                "max_tokens": 128000,
                "supports_function_calling": True
            }
        },
        
        {
            "model_name": "llama-3-1-8b",
            "litellm_params": {
                "model": "openai/meta-llama/llama-3.1-8b-instruct",
                "api_base": "https://api.aimlapi.com/v1",
                "api_key": "os.environ/AIMLAPI_KEY"
            },
            "model_info": {
                "description": "Llama 3.1 8B - Fast and efficient",
                "provider": "aimlapi",
                "max_tokens": 128000,
                "supports_function_calling": True
            }
        },
        
        # Anthropic Claude Models
        {
            "model_name": "claude-3-haiku",
            "litellm_params": {
                "model": "openai/claude-3-haiku-20240307",
                "api_base": "https://api.aimlapi.com/v1",
                "api_key": "os.environ/AIMLAPI_KEY"
            },
            "model_info": {
                "description": "Claude 3 Haiku - Fast and cost-effective",
                "provider": "aimlapi",
                "max_tokens": 200000,
                "supports_function_calling": True
            }
        },
        
        # Google Gemini Models
        {
            "model_name": "gemini-1-5-flash",
            "litellm_params": {
                "model": "openai/gemini-1.5-flash-latest",
                "api_base": "https://api.aimlapi.com/v1",
                "api_key": "os.environ/AIMLAPI_KEY"
            },
            "model_info": {
                "description": "Gemini 1.5 Flash - Google's fast model",
                "provider": "aimlapi",
                "max_tokens": 1048576,
                "supports_function_calling": True
            }
        },
        
        # Mistral Models
        {
            "model_name": "mixtral-8x7b",
            "litellm_params": {
                "model": "openai/mistralai/mixtral-8x7b-instruct-v0.1",
                "api_base": "https://api.aimlapi.com/v1",
                "api_key": "os.environ/AIMLAPI_KEY"
            },
            "model_info": {
                "description": "Mixtral 8x7B - Mixture of experts model",
                "provider": "aimlapi",
                "max_tokens": 32768,
                "supports_function_calling": True
            }
        }
    ]
    
    print(f"🚀 Thêm {len(models_to_add)} models vào LiteLLM...")
    print("="*60)
    
    success_count = 0
    for model_config in models_to_add:
        try:
            response = requests.post(f"{base_url}/model/new", 
                                   headers=headers, 
                                   json=model_config)
            response.raise_for_status()
            print(f"✅ Đã thêm: {model_config['model_name']}")
            success_count += 1
        except Exception as e:
            print(f"❌ Lỗi khi thêm {model_config['model_name']}: {e}")
    
    print("="*60)
    print(f"📊 Kết quả: {success_count}/{len(models_to_add)} models được thêm thành công")
    
    return success_count

def main():
    add_models_from_list()

if __name__ == "__main__":
    main()

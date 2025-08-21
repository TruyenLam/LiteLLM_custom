#!/usr/bin/env python3
"""
🚀 SHAREAPIAI.COM - ADVANCED MODEL MANAGER
Quản lý models từ AIMLAPI và LiteLLM Container
"""

import requests
import json
import os
import time
import random
from datetime import datetime
from typing import List, Dict, Any
import yaml

class ShareAPIAIModelManager:
    def __init__(self):
        self.aimlapi_key = "b0197edcd9104cd1ab78aaf148ce609a"
        self.litellm_base_url = "https://call.shareapiai.com"
        self.litellm_api_key = "sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1"
        self.models_file = "shareapiai_models_info.json"
        
        # Headers for AIMLAPI
        self.aimlapi_headers = {
            "Authorization": f"Bearer {self.aimlapi_key}",
            "Content-Type": "application/json"
        }
        
        # Headers for LiteLLM
        self.litellm_headers = {
            "Authorization": f"Bearer {self.litellm_api_key}",
            "Content-Type": "application/json"
        }
    
    def fetch_latest_models_from_aimlapi(self) -> List[Dict]:
        """
        🔄 CHỨC NĂNG 1: Lấy thông tin models mới nhất từ AIMLAPI
        """
        print("🔄 Đang lấy danh sách models mới nhất từ AIMLAPI...")
        
        try:
            response = requests.get(
                "https://api.aimlapi.com/models",
                headers=self.aimlapi_headers,
                timeout=30
            )
            response.raise_for_status()
            
            models_data = response.json()
            models = models_data.get('data', [])
            
            # Thêm thông tin shareapiai.com vào mỗi model
            enhanced_models = []
            for model in models:
                enhanced_model = {
                    "id": model.get('id', ''),
                    "object": model.get('object', 'model'),
                    "created": model.get('created', int(time.time())),
                    "owned_by": model.get('owned_by', 'aimlapi'),
                    "description": f"{model.get('id', '')} - Provided by shareapiai.com ",
                    "provider": "shareapiai.com",
                    "shareapiai_enhanced": True,
                    "shareapiai_added_date": datetime.now().isoformat(),
                    "api_base": "https://api.aimlapi.com/v1",
                    "max_tokens": self._get_model_max_tokens(model.get('id', '')),
                    "supports_function_calling": self._supports_function_calling(model.get('id', '')),
                    "supports_vision": self._supports_vision(model.get('id', '')),
                    "model_type": self._get_model_type(model.get('id', ''))
                }
                enhanced_models.append(enhanced_model)
            
            # Lưu vào file
            models_info = {
                "updated_at": datetime.now().isoformat(),
                "source": "https://api.aimlapi.com/models",
                "enhanced_by": "shareapiai.com",
                "total_models": len(enhanced_models),
                "models": enhanced_models
            }
            
            with open(self.models_file, 'w', encoding='utf-8') as f:
                json.dump(models_info, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Đã lưu {len(enhanced_models)} models vào {self.models_file}")
            print(f"📁 File được cập nhật lúc: {models_info['updated_at']}")
            
            return enhanced_models
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi khi lấy models từ AIMLAPI: {e}")
            return []
        except Exception as e:
            print(f"❌ Lỗi không xác định: {e}")
            return []
    
    def _get_model_max_tokens(self, model_id: str) -> int:
        """Ước tính max tokens dựa trên model name"""
        model_id = model_id.lower()
        if 'gpt-4' in model_id:
            if 'turbo' in model_id or '1106' in model_id or '0125' in model_id:
                return 128000
            return 8192
        elif 'gpt-3.5' in model_id:
            if 'turbo' in model_id and ('1106' in model_id or '0125' in model_id):
                return 16385
            return 4096
        elif 'claude' in model_id:
            if 'claude-3' in model_id:
                return 200000
            return 100000
        elif 'gemini' in model_id:
            if '1.5' in model_id:
                return 2097152
            return 32768
        elif 'llama' in model_id:
            if '70b' in model_id or '405b' in model_id:
                return 128000
            return 8192
        else:
            return 4096
    
    def _supports_function_calling(self, model_id: str) -> bool:
        """Kiểm tra model có hỗ trợ function calling không"""
        model_id = model_id.lower()
        function_calling_models = [
            'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini-1.5', 
            'llama-3.1', 'mistral', 'command-r'
        ]
        return any(model_name in model_id for model_name in function_calling_models)
    
    def _supports_vision(self, model_id: str) -> bool:
        """Kiểm tra model có hỗ trợ vision không"""
        model_id = model_id.lower()
        vision_models = [
            'gpt-4o', 'gpt-4-vision', 'claude-3', 'gemini-1.5-pro',
            'llava', 'qwen-vl'
        ]
        return any(model_name in model_id for model_name in vision_models)
    
    def _get_model_type(self, model_id: str) -> str:
        """Xác định loại model"""
        model_id = model_id.lower()
        if any(x in model_id for x in ['gpt', 'openai']):
            return 'openai'
        elif 'claude' in model_id:
            return 'anthropic'
        elif 'gemini' in model_id:
            return 'google'
        elif 'llama' in model_id:
            return 'meta'
        elif 'mistral' in model_id:
            return 'mistral'
        elif 'command' in model_id:
            return 'cohere'
        else:
            return 'other'
    
    def get_current_litellm_models(self) -> List[str]:
        """Lấy danh sách models hiện tại trong LiteLLM"""
        try:
            response = requests.get(
                f"{self.litellm_base_url}/v1/models",
                headers=self.litellm_headers,
                timeout=30
            )
            response.raise_for_status()
            
            models_data = response.json()
            return [model['id'] for model in models_data.get('data', [])]
            
        except Exception as e:
            print(f"❌ Lỗi khi lấy models từ LiteLLM: {e}")
            return []
    
    def update_models_to_container(self) -> None:
        """
        🔄 CHỨC NĂNG 2: Cập nhật models từ file vào container
        """
        print("🔄 Đang cập nhật models vào LiteLLM container...")
        
        # Đọc file models
        if not os.path.exists(self.models_file):
            print(f"❌ File {self.models_file} không tồn tại. Chạy chức năng 1 trước!")
            return
        
        try:
            with open(self.models_file, 'r', encoding='utf-8') as f:
                models_info = json.load(f)
            
            available_models = models_info.get('models', [])
            current_models = self.get_current_litellm_models()
            
            print(f"📊 Có {len(available_models)} models trong file")
            print(f"📊 Có {len(current_models)} models trong container")
            
            # Danh sách models phổ biến để ưu tiên thêm
            priority_models = [
                'gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-3.5-turbo',
                'claude-3-5-sonnet', 'claude-3-opus', 'claude-3-haiku',
                'gemini-1.5-pro', 'gemini-1.5-flash',
                'llama-3.1-405b', 'llama-3.1-70b', 'llama-3.1-8b',
                'mistral-large', 'command-r-plus'
            ]
            
            added_count = 0
            updated_count = 0
            
            for model in available_models:
                model_id = model.get('id', '')
                
                # Ưu tiên models phổ biến
                is_priority = any(priority in model_id.lower() for priority in priority_models)
                
                if not is_priority and added_count >= 200:  # Giới hạn 20 models để tránh quá tải
                    continue
                
                if model_id in current_models:
                    print(f"🔄 Model {model_id} đã tồn tại, bỏ qua...")
                    updated_count += 1
                    continue
                
                # Thêm model mới
                litellm_config = {
                    "model_name": model_id,
                    "litellm_params": {
                        "model": f"openai/{model_id}",
                        "api_base": model.get('api_base', 'https://api.aimlapi.com/v1'),
                        "api_key": "os.environ/AIMLAPI_KEY"
                    },
                    "model_info": {
                        "description": model.get('description', f"{model_id} via shareapiai.com"),
                        "provider": "shareapi",
                        "max_tokens": model.get('max_tokens', 4096),
                        "supports_function_calling": model.get('supports_function_calling', False),
                        "supports_vision": model.get('supports_vision', False),
                        "model_type": model.get('model_type', 'other'),
                        "shareapiai_enhanced": True
                    }
                }
                
                try:
                    response = requests.post(
                        f"{self.litellm_base_url}/model/new",
                        headers=self.litellm_headers,
                        json=litellm_config,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        print(f"✅ Đã thêm model: {model_id}")
                        added_count += 1
                    else:
                        print(f"⚠️ Không thể thêm {model_id}: {response.status_code}")
                        
                except Exception as e:
                    print(f"❌ Lỗi khi thêm {model_id}: {e}")
                
                # Delay để tránh rate limit
                time.sleep(0.5)
            
            print(f"\n📊 KẾT QUẢ CẬP NHẬT:")
            print(f"✅ Đã thêm mới: {added_count} models")
            print(f"🔄 Đã tồn tại: {updated_count} models")
            
        except Exception as e:
            print(f"❌ Lỗi khi cập nhật models: {e}")
    
    def test_model(self, model_name: str = None) -> None:
        """
        🧪 CHỨC NĂNG 3: Test model
        """
        if not model_name:
            # Hiển thị danh sách models để chọn
            current_models = self.get_current_litellm_models()
            if not current_models:
                print("❌ Không có models nào trong container!")
                return
            
            print("📊 DANH SÁCH MODELS HIỆN TẠI:")
            for i, model in enumerate(current_models, 1):
                print(f" {i}. {model}")
            
            try:
                choice = input("\nNhập số thứ tự model để test (hoặc nhập tên model): ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(current_models):
                        model_name = current_models[idx]
                    else:
                        print("❌ Số thứ tự không hợp lệ!")
                        return
                else:
                    model_name = choice
            except KeyboardInterrupt:
                print("\n👋 Đã hủy test!")
                return
        
        print(f"🧪 Đang test model: {model_name}")
        
        # Test cơ bản
        test_payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user", 
                    "content": "Hello! Please respond with 'I am working correctly via shareapiai.com'"
                }
            ],
            "max_tokens": 50,
            "temperature": 0.1
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.litellm_base_url}/v1/chat/completions",
                headers=self.litellm_headers,
                json=test_payload,
                timeout=60
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                usage = result.get('usage', {})
                
                print(f"✅ Model {model_name} hoạt động bình thường!")
                print(f"📝 Phản hồi: {content}")
                print(f"⏱️ Thời gian phản hồi: {end_time - start_time:.2f}s")
                print(f"🔢 Tokens sử dụng: {usage.get('total_tokens', 'N/A')}")
                
                # Test function calling nếu hỗ trợ
                self._test_function_calling(model_name)
                
            else:
                print(f"❌ Model {model_name} lỗi: {response.status_code}")
                print(f"📄 Chi tiết: {response.text}")
                
        except Exception as e:
            print(f"❌ Lỗi khi test model {model_name}: {e}")
    
    def _test_function_calling(self, model_name: str) -> None:
        """Test function calling capability"""
        print(f"🔧 Đang test function calling cho {model_name}...")
        
        test_payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": "What's the weather like in Hanoi?"}
            ],
            "functions": [
                {
                    "name": "get_weather",
                    "description": "Get current weather information for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name"
                            }
                        },
                        "required": ["location"]
                    }
                }
            ],
            "max_tokens": 100
        }
        
        try:
            response = requests.post(
                f"{self.litellm_base_url}/v1/chat/completions",
                headers=self.litellm_headers,
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']
                
                if 'function_call' in message:
                    print(f"✅ Function calling hoạt động!")
                    print(f"🔧 Function: {message['function_call']['name']}")
                else:
                    print(f"⚠️ Function calling không được sử dụng (có thể model không hỗ trợ)")
            else:
                print(f"⚠️ Function calling test thất bại: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Không thể test function calling: {e}")
    
    def delete_model(self, model_name: str = None) -> None:
        """
        🗑️ CHỨC NĂNG 4: Xóa model
        """
        if not model_name:
            # Hiển thị danh sách models để chọn
            current_models = self.get_current_litellm_models()
            if not current_models:
                print("❌ Không có models nào trong container!")
                return
            
            print("📊 DANH SÁCH MODELS HIỆN TẠI:")
            for i, model in enumerate(current_models, 1):
                print(f" {i}. {model}")
            
            try:
                choice = input("\nNhập số thứ tự model để xóa (hoặc nhập tên model): ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(current_models):
                        model_name = current_models[idx]
                    else:
                        print("❌ Số thứ tự không hợp lệ!")
                        return
                else:
                    model_name = choice
            except KeyboardInterrupt:
                print("\n👋 Đã hủy xóa!")
                return
        
        # Xác nhận xóa
        confirm = input(f"⚠️ Bạn có chắc muốn xóa model '{model_name}'? (y/N): ").strip().lower()
        if confirm != 'y':
            print("👋 Đã hủy xóa!")
            return
        
        print(f"🗑️ Đang thử xóa model: {model_name}")
        
        # Thử các phương pháp xóa model
        success = False
        
        # Phương pháp 1: DELETE /model/{model_name}
        try:
            print("🔄 Phương pháp 1: DELETE /model/{model_name}")
            response = requests.delete(
                f"{self.litellm_base_url}/model/{model_name}",
                headers=self.litellm_headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Đã xóa model {model_name} thành công!")
                success = True
            elif response.status_code == 404:
                print(f"⚠️ API trả về 404 - Model không tồn tại hoặc không thể xóa")
            elif response.status_code == 405:
                print(f"⚠️ Method không được hỗ trợ")
            else:
                print(f"⚠️ API trả về status: {response.status_code}")
                print(f"📄 Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Lỗi khi gọi DELETE API: {e}")
        
        if not success:
            # Phương pháp 2: POST /model/delete
            try:
                print("🔄 Phương pháp 2: POST /model/delete")
                response = requests.post(
                    f"{self.litellm_base_url}/model/delete",
                    headers=self.litellm_headers,
                    json={"model_name": model_name},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ Đã xóa model {model_name} thành công!")
                    success = True
                else:
                    print(f"⚠️ POST delete trả về status: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Lỗi khi gọi POST delete: {e}")
        
        if not success:
            # Phương pháp 3: PUT /model/update với action delete
            try:
                print("🔄 Phương pháp 3: PUT /model/update")
                response = requests.put(
                    f"{self.litellm_base_url}/model/update",
                    headers=self.litellm_headers,
                    json={"model_name": model_name, "action": "delete"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ Đã xóa model {model_name} thành công!")
                    success = True
                else:
                    print(f"⚠️ PUT update trả về status: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Lỗi khi gọi PUT update: {e}")
        
        if not success:
            print(f"\n❌ KHÔNG THỂ XÓA MODEL QUA API")
            print(f"🔍 LiteLLM có thể không hỗ trợ xóa models qua REST API")
            
        # Hướng dẫn xóa thủ công
        print(f"\n📋 HƯỚNG DẪN XÓA MODEL THỦ CÔNG:")
        print(f"1. 🔄 Restart container để reset tất cả models:")
        print(f"   az containerapp revision restart --name litellm-app --resource-group rg-litellm")
        print(f"2. 🛑 Stop và Start lại container:")
        print(f"   az containerapp stop --name litellm-app --resource-group rg-litellm")
        print(f"   az containerapp start --name litellm-app --resource-group rg-litellm")
        print(f"3. 🌐 Qua Azure Portal:")
        print(f"   Container Apps → litellm-app → Restart")
        print(f"4. ➕ Sau đó chạy lại chức năng 2 để thêm lại models cần thiết")
        
        # Kiểm tra model còn tồn tại không
        print(f"\n🔍 Kiểm tra model sau khi thử xóa...")
        remaining_models = self.get_current_litellm_models()
        if model_name in remaining_models:
            print(f"⚠️ Model {model_name} vẫn còn trong container")
        else:
            print(f"✅ Model {model_name} đã không còn trong danh sách!")
    
    def delete_all_models(self) -> None:
        """
        🗑️ CHỨC NĂNG 5: Xóa toàn bộ models
        """
        print("🗑️ XÓA TOÀN BỘ MODELS")
        print("="*50)
        
        # Lấy danh sách models hiện tại
        current_models = self.get_current_litellm_models()
        if not current_models:
            print("❌ Không có models nào trong container!")
            return
        
        print(f"📊 Hiện tại có {len(current_models)} models trong container:")
        for i, model in enumerate(current_models[:10], 1):
            print(f"  {i}. {model}")
        if len(current_models) > 10:
            print(f"  ... và {len(current_models) - 10} models khác")
        
        print("\n⚠️  CẢNH BÁO: Bạn sắp xóa TOÀN BỘ models!")
        print("⚠️  Hành động này KHÔNG THỂ HOÀN TÁC!")
        print("⚠️  Container sẽ không có models nào sau khi xóa!")
        
        # Xác nhận lần 1
        confirm1 = input("\n🤔 Bạn có chắc muốn xóa TOÀN BỘ models? (yes/NO): ").strip()
        if confirm1.lower() != 'yes':
            print("👋 Đã hủy xóa toàn bộ models!")
            return
        
        # Xác nhận lần 2 với captcha
        captcha = random.randint(1000, 9999)
        print(f"\n🔐 Để xác nhận, vui lòng nhập số: {captcha}")
        captcha_input = input("Nhập số xác nhận: ").strip()
        
        if captcha_input != str(captcha):
            print("❌ Số xác nhận không đúng! Đã hủy xóa.")
            return
        
        print("\n🗑️ Bắt đầu xóa toàn bộ models...")
        
        # Phương pháp 1: Thử xóa từng model qua API
        deleted_count = 0
        failed_count = 0
        
        for i, model in enumerate(current_models, 1):
            print(f"🗑️ Đang xóa {i}/{len(current_models)}: {model}")
            
            try:
                # Thử DELETE request
                response = requests.delete(
                    f"{self.litellm_base_url}/model/{model}",
                    headers=self.litellm_headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"  ✅ Đã xóa: {model}")
                    deleted_count += 1
                elif response.status_code == 404:
                    print(f"  ⚠️ Không tồn tại: {model}")
                    deleted_count += 1
                elif response.status_code == 405:
                    print(f"  ⚠️ API không hỗ trợ xóa: {model}")
                    failed_count += 1
                else:
                    print(f"  ❌ Lỗi {response.status_code}: {model}")
                    failed_count += 1
                    
            except Exception as e:
                print(f"  ❌ Lỗi khi xóa {model}: {e}")
                failed_count += 1
            
            # Delay để tránh rate limit
            time.sleep(0.2)
        
        print(f"\n📊 KẾT QUẢ XÓA TOÀN BỘ MODELS:")
        print(f"✅ Đã xóa: {deleted_count} models")
        print(f"❌ Thất bại: {failed_count} models")
        
        if failed_count > 0:
            print(f"\n📋 HƯỚNG DẪN XÓA TOÀN BỘ MODELS THỦ CÔNG:")
            print(f"1. Restart container để reset tất cả models:")
            print(f"   az containerapp revision restart --name litellm-app --resource-group rg-litellm")
            print(f"2. Hoặc stop và start lại container:")
            print(f"   az containerapp stop --name litellm-app --resource-group rg-litellm")
            print(f"   az containerapp start --name litellm-app --resource-group rg-litellm")
            print(f"3. Container sẽ khởi động với 0 models")
            print(f"4. Chạy chức năng 2 để thêm lại models cần thiết")
        
        # Kiểm tra lại sau khi xóa
        print(f"\n🔍 Kiểm tra lại models còn lại...")
        remaining_models = self.get_current_litellm_models()
        if remaining_models:
            print(f"⚠️ Còn lại {len(remaining_models)} models:")
            for model in remaining_models[:5]:
                print(f"  - {model}")
            if len(remaining_models) > 5:
                print(f"  ... và {len(remaining_models) - 5} models khác")
        else:
            print(f"✅ Container đã sạch, không còn models nào!")


def main():
    manager = ShareAPIAIModelManager()
    
    while True:
        print("\n" + "="*60)
        print("🚀 SHAREAPIAI.COM - ADVANCED MODEL MANAGER")
        print("="*60)
        print("1. 📥 Lấy models mới nhất từ AIMLAPI và lưu file")
        print("2. 🔄 Cập nhật models từ file vào container")
        print("3. 🧪 Test model")
        print("4. 🗑️ Xóa model")
        print("5. 🧹 Xóa toàn bộ models")
        print("6. 📊 Xem thông tin file models")
        print("7. 📋 Xem models hiện tại trong container")
        print("0. 👋 Thoát")
        print("="*60)
        
        try:
            choice = input("Chọn chức năng (0-7): ").strip()
            
            if choice == "0":
                print("👋 Tạm biệt!")
                break
            elif choice == "1":
                print("\n🔄 CHỨC NĂNG 1: LẤY MODELS TỪ AIMLAPI")
                models = manager.fetch_latest_models_from_aimlapi()
                if models:
                    print(f"✅ Đã lấy và lưu {len(models)} models!")
            
            elif choice == "2":
                print("\n🔄 CHỨC NĂNG 2: CẬP NHẬT MODELS VÀO CONTAINER")
                manager.update_models_to_container()
            
            elif choice == "3":
                print("\n🧪 CHỨC NĂNG 3: TEST MODEL")
                manager.test_model()
            
            elif choice == "4":
                print("\n🗑️ CHỨC NĂNG 4: XÓA MODEL")
                manager.delete_model()
            
            elif choice == "5":
                print("\n🧹 CHỨC NĂNG 5: XÓA TOÀN BỘ MODELS")
                manager.delete_all_models()
            
            elif choice == "6":
                print("\n📊 THÔNG TIN FILE MODELS:")
                if os.path.exists(manager.models_file):
                    with open(manager.models_file, 'r', encoding='utf-8') as f:
                        models_info = json.load(f)
                    print(f"📅 Cập nhật lần cuối: {models_info.get('updated_at', 'N/A')}")
                    print(f"🔗 Nguồn: {models_info.get('source', 'N/A')}")
                    print(f"🏷️ Enhanced by: {models_info.get('enhanced_by', 'N/A')}")
                    print(f"📊 Tổng models: {models_info.get('total_models', 0)}")
                else:
                    print("❌ File models chưa tồn tại. Chạy chức năng 1 trước!")
            
            elif choice == "7":
                print("\n📋 MODELS HIỆN TẠI TRONG CONTAINER:")
                current_models = manager.get_current_litellm_models()
                if current_models:
                    for i, model in enumerate(current_models, 1):
                        print(f" {i}. {model}")
                    print(f"\n📊 Tổng: {len(current_models)} models")
                else:
                    print("❌ Không có models nào trong container!")
            
            else:
                print("❌ Lựa chọn không hợp lệ!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Azure Container App Updater for LiteLLM
Cập nhật cấu hình models vào Azure Container App
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any

class AzureContainerAppUpdater:
    def __init__(self, resource_group: str = "rg-litellm", app_name: str = "litellm-app"):
        self.resource_group = resource_group
        self.app_name = app_name
        
    def check_azure_cli(self) -> bool:
        """Kiểm tra Azure CLI có sẵn không"""
        try:
            result = subprocess.run(['az', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def get_current_config(self) -> Dict[str, Any]:
        """Lấy cấu hình hiện tại của container app"""
        try:
            cmd = [
                'az', 'containerapp', 'show',
                '--name', self.app_name,
                '--resource-group', self.resource_group,
                '--query', 'properties.template'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi khi lấy cấu hình: {e}")
            return {}
    
    def create_config_volume_mount(self, config_content: str) -> Dict[str, Any]:
        """Tạo volume mount cho config file"""
        
        # Tạo cấu hình cho Azure File Share (nếu cần)
        volume_config = {
            "volumes": [
                {
                    "name": "config-volume",
                    "storageType": "EmptyDir"
                }
            ],
            "containers": [
                {
                    "name": self.app_name,
                    "volumeMounts": [
                        {
                            "volumeName": "config-volume",
                            "mountPath": "/app/config"
                        }
                    ]
                }
            ]
        }
        
        return volume_config
    
    def update_environment_variables(self, additional_env: Dict[str, str] = None):
        """Cập nhật environment variables"""
        try:
            # Lấy env vars hiện tại
            current_env = self.get_current_env_vars()
            
            # Thêm env vars mới nếu có
            if additional_env:
                current_env.update(additional_env)
            
            # Tạo command để update
            env_args = []
            for key, value in current_env.items():
                env_args.extend(['--set-env-vars', f'{key}={value}'])
            
            cmd = [
                'az', 'containerapp', 'update',
                '--name', self.app_name,
                '--resource-group', self.resource_group
            ] + env_args
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("✅ Đã cập nhật environment variables")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi khi cập nhật env vars: {e}")
            return False
    
    def get_current_env_vars(self) -> Dict[str, str]:
        """Lấy environment variables hiện tại"""
        try:
            cmd = [
                'az', 'containerapp', 'show',
                '--name', self.app_name,
                '--resource-group', self.resource_group,
                '--query', 'properties.template.containers[0].env'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            env_list = json.loads(result.stdout)
            
            # Convert to dict
            env_dict = {}
            if env_list:
                for env_var in env_list:
                    env_dict[env_var['name']] = env_var.get('value', '')
            
            return env_dict
            
        except subprocess.CalledProcessError:
            return {}
    
    def restart_container_app(self):
        """Restart container app để áp dụng config mới"""
        try:
            cmd = [
                'az', 'containerapp', 'revision', 'restart',
                '--name', self.app_name,
                '--resource-group', self.resource_group
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("✅ Đã restart container app")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi khi restart: {e}")
            return False
    
    def update_with_config_file(self, config_file_path: str):
        """Cập nhật container app với config file"""
        try:
            # Đọc config file
            with open(config_file_path, 'r', encoding='utf-8') as f:
                if config_file_path.endswith('.json'):
                    config = json.load(f)
                else:
                    import yaml
                    config = yaml.safe_load(f)
            
            print(f"📁 Đã đọc config từ {config_file_path}")
            
            # Cập nhật environment với số lượng models
            model_count = len(config.get('model_list', []))
            additional_env = {
                'LITELLM_CONFIG_MODELS_COUNT': str(model_count),
                'LITELLM_CONFIG_SOURCE': 'aimlapi_auto_generated'
            }
            
            # Update env vars
            self.update_environment_variables(additional_env)
            
            print(f"✅ Đã cập nhật với {model_count} models từ AIMLAPI")
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi cập nhật config: {e}")
            return False
    
    def get_app_status(self):
        """Lấy trạng thái của container app"""
        try:
            cmd = [
                'az', 'containerapp', 'show',
                '--name', self.app_name,
                '--resource-group', self.resource_group,
                '--query', '{RunningStatus:properties.runningStatus, LatestRevision:properties.latestRevisionName, FQDN:properties.configuration.ingress.fqdn}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            status = json.loads(result.stdout)
            
            print("\n📊 TRẠNG THÁI CONTAINER APP:")
            print(f"   Status: {status.get('RunningStatus', 'Unknown')}")
            print(f"   Revision: {status.get('LatestRevision', 'Unknown')}")
            print(f"   URL: https://{status.get('FQDN', 'Unknown')}")
            
            return status
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi khi lấy status: {e}")
            return {}

def main():
    """Main function"""
    print("🔄 Azure Container App Updater for LiteLLM")
    print("="*50)
    
    updater = AzureContainerAppUpdater()
    
    # Check Azure CLI
    if not updater.check_azure_cli():
        print("❌ Azure CLI không có sẵn. Vui lòng cài đặt Azure CLI.")
        return
    
    # Check config files
    config_files = [
        "aimlapi_litellm_config.yaml",
        "aimlapi_litellm_config.json"
    ]
    
    config_file = None
    for file_path in config_files:
        if Path(file_path).exists():
            config_file = file_path
            break
    
    if not config_file:
        print("❌ Không tìm thấy config file. Chạy fetch_aimlapi_models.py trước.")
        return
    
    print(f"📁 Sử dụng config file: {config_file}")
    
    # Get current status
    updater.get_app_status()
    
    # Update with config
    print("\n🔄 Đang cập nhật container app...")
    success = updater.update_with_config_file(config_file)
    
    if success:
        print("\n🎉 CẬP NHẬT THÀNH CÔNG!")
        print("\n🚀 BƯỚC TIẾP THEO:")
        print("   1. Kiểm tra logs: az containerapp logs show --name litellm-app --resource-group rg-litellm")
        print("   2. Test API: curl https://call.shareapiai.com/health/liveliness")
        print("   3. Kiểm tra models: curl https://call.shareapiai.com/v1/models")
        
        # Get updated status
        print("\n" + "="*50)
        updater.get_app_status()
    else:
        print("\n❌ CẬP NHẬT THẤT BẠI!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Environment Override for LiteLLM Free Version
Ensures all enterprise features are disabled
"""

import os

def setup_free_environment():
    """Configure environment for maximum compatibility without enterprise features"""
    
    # Core LiteLLM settings
    overrides = {
        # Disable enterprise licensing
        "LITELLM_LICENSE": "",
        "LITELLM_ENTERPRISE": "false",
        
        # Disable telemetry and tracking
        "LITELLM_DISABLE_TELEMETRY": "true",
        "DISABLE_TELEMETRY": "true",
        
        # Disable enterprise metrics
        "DISABLE_PROMETHEUS": "true", 
        "LITELLM_DISABLE_PROMETHEUS": "true",
        "DISABLE_SPEND_LOGS": "true",
        "LITELLM_DISABLE_SPEND_LOGS": "true",
        
        # Disable enterprise features
        "DISABLE_ENTERPRISE_FEATURES": "true",
        "LITELLM_DISABLE_ENTERPRISE": "true",
        
        # Logging settings
        "LITELLM_LOG_LEVEL": "INFO",
        "LITELLM_VERBOSE": "false",
        
        # Custom budget system
        "ENABLE_CUSTOM_BUDGET": "true",
        "USE_CUSTOM_CALLBACKS": "true",
        
        # Performance settings
        "LITELLM_REQUEST_TIMEOUT": "300",
        "LITELLM_NUM_RETRIES": "3",
        
        # UI settings (if applicable)
        "LITELLM_UI_ACCESS": "admin_only",
        
        # Database settings
        "STORE_MODEL_IN_DB": os.getenv("STORE_MODEL_IN_DB", "True"),
        
        # Health check settings
        "HEALTH_CHECK_INTERVAL": "300"
    }
    
    # Apply environment overrides
    for key, value in overrides.items():
        os.environ[key] = value
        print(f"✅ Set {key}={value}")
    
    # Preserve existing important variables
    important_vars = [
        "AIMLAPI_KEY",
        "LITELLM_MASTER_KEY", 
        "LITELLM_SALT_KEY",
        "DATABASE_URL",
        "PORT",
        "HOST"
    ]
    
    print("\n📋 Important environment variables:")
    for var in important_vars:
        value = os.getenv(var, "NOT_SET")
        if var in ["AIMLAPI_KEY", "LITELLM_MASTER_KEY", "LITELLM_SALT_KEY"]:
            # Mask sensitive values
            masked = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            print(f"   {var}={masked}")
        else:
            print(f"   {var}={value}")

def create_minimal_config():
    """Create minimal configuration file without enterprise features"""
    config_content = """
# Minimal LiteLLM Configuration - Free Version
# All enterprise features disabled

model_list:
  # Models from config file will be loaded here
  
litellm_settings:
  drop_params: true
  num_retries: 3
  request_timeout: 300
  telemetry: false
  # No enterprise callbacks

general_settings:
  store_model_in_db: true
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
  
  # Health and logging
  health_check_interval: 300
  set_verbose: false
  
  # Completely disable enterprise
  disable_spend_logs: true
  disable_prometheus_metrics: true
  ui_access_mode: "admin_only"
  
  # Custom tracking
  track_cost_per_request: false  # Use our custom system instead
"""
    
    return config_content.strip()

if __name__ == "__main__":
    print("🔧 Setting up LiteLLM Free Environment")
    setup_free_environment()
    print("\n✅ Environment configured for free version")
    
    # Show sample config
    print("\n📄 Minimal config structure:")
    print(create_minimal_config())

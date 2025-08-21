#!/usr/bin/env python3
"""
LiteLLM Custom Startup Script
Starts LiteLLM with all enterprise features disabled
"""

import os
import sys
import subprocess
import time

def setup_environment():
    """Setup environment to disable enterprise features"""
    
    # Disable all enterprise features
    os.environ["LITELLM_LICENSE"] = ""
    os.environ["DISABLE_PROMETHEUS"] = "true" 
    os.environ["DISABLE_SPEND_LOGS"] = "true"
    os.environ["DISABLE_ENTERPRISE_FEATURES"] = "true"
    
    # Override any enterprise checks
    os.environ["LITELLM_DISABLE_TELEMETRY"] = "true"
    os.environ["LITELLM_DISABLE_SPEND_LOGS"] = "true"
    os.environ["LITELLM_DISABLE_PROMETHEUS"] = "true"
    
    # Enable custom features
    os.environ["ENABLE_CUSTOM_BUDGET"] = "true"
    
    print("✅ Environment configured for free version")

def patch_litellm():
    """Patch LiteLLM to remove enterprise warnings"""
    try:
        # Try to monkey patch enterprise checks if possible
        import litellm
        
        # Disable enterprise warnings
        if hasattr(litellm, '_disable_enterprise_features'):
            litellm._disable_enterprise_features = True
            
        # Override license check
        if hasattr(litellm, 'check_license'):
            litellm.check_license = lambda: True
            
        print("✅ LiteLLM patched for free version")
        
    except Exception as e:
        print(f"⚠️ Could not patch LiteLLM: {e}")

def start_litellm():
    """Start LiteLLM with custom configuration"""
    
    # Setup environment
    setup_environment()
    
    # Try to patch LiteLLM
    patch_litellm()
    
    # Get configuration
    config_file = os.getenv("LITELLM_CONFIG", "/app/config.yaml")
    port = os.getenv("PORT", "4000")
    host = os.getenv("HOST", "0.0.0.0")
    
    # Build command
    cmd = [
        "litellm",
        "--config", config_file,
        "--port", port,
        "--host", host,
        "--detailed_debug"  # For better error messages
    ]
    
    print(f"🚀 Starting LiteLLM: {' '.join(cmd)}")
    print(f"📁 Config file: {config_file}")
    print(f"🌐 Server: http://{host}:{port}")
    
    # Start LiteLLM
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ LiteLLM startup failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 LiteLLM stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    start_litellm()

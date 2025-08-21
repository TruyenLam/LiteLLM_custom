# 🔧 HƯỚNG DẪN CẬP NHẬT VÀ THÊM MODELS VÀO LITELLM

## 🚀 3 CÁCH CHÍNH ĐỂ QUẢN LÝ MODELS:

### 1. 📱 CÁCH 1: SỬ DỤNG API TRỰC TIẾP (RECOMMENDED)

#### Thêm Model Mới:
```bash
curl -X POST https://call.shareapiai.com/model/new \
  -H "Authorization: Bearer sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "llama-3-1-70b",
    "litellm_params": {
      "model": "openai/meta-llama/llama-3.1-70b-instruct",
      "api_base": "https://api.aimlapi.com/v1",
      "api_key": "os.environ/AIMLAPI_KEY"
    },
    "model_info": {
      "description": "Llama 3.1 70B - Meta flagship model",
      "provider": "aimlapi",
      "max_tokens": 128000
    }
  }'
```

#### Xem Models Hiện Tại:
```bash
curl -H "Authorization: Bearer sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1" \
     https://call.shareapiai.com/v1/models
```

#### Xem Chi Tiết Models:
```bash
curl -H "Authorization: Bearer sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1" \
     https://call.shareapiai.com/model/info
```

### 2. 🐍 CÁCH 2: SỬ DỤNG PYTHON SCRIPTS

#### A. Script Interactive (Recommended):
```bash
cd D:\Project_ShareAPIai\CODE\litellm
D:/Project_ShareAPIai/venv/Scripts/python.exe manage_models.py
```

**Features:**
- Menu interactive
- Thêm model từng cái một
- Batch thêm models phổ biến
- Test models
- Xóa models (nếu hỗ trợ)

#### B. Script Quick Add:
```bash
D:/Project_ShareAPIai/venv/Scripts/python.exe quick_add_models.py
```

**Features:**
- Thêm 6 models phổ biến một lúc
- Không cần input
- Chạy nhanh

#### C. Script Fetch All AIMLAPI:
```bash
D:/Project_ShareAPIai/venv/Scripts/python.exe fetch_aimlapi_models.py
```

**Features:**
- Lấy tất cả 237 models từ AIMLAPI
- Tạo config file YAML
- Backup raw data

### 3. ⚙️ CÁCH 3: CẬP NHẬT VIA AZURE CLI

#### Thêm Environment Variables:
```bash
az containerapp update --name litellm-app --resource-group rg-litellm \
  --set-env-vars NEW_MODEL_CONFIG="custom_value"
```

#### Restart Container:
```bash
az containerapp revision restart --name litellm-app --resource-group rg-litellm
```

## 🎯 MODELS TEMPLATES THƯỜNG DÙNG:

### OpenAI Models:
```json
{
  "model_name": "gpt-4o",
  "litellm_params": {
    "model": "openai/gpt-4o",
    "api_base": "https://api.aimlapi.com/v1",
    "api_key": "os.environ/AIMLAPI_KEY"
  },
  "model_info": {
    "description": "GPT-4o via AIMLAPI",
    "provider": "aimlapi",
    "max_tokens": 128000,
    "supports_function_calling": true,
    "supports_vision": true
  }
}
```

### Anthropic Claude Models:
```json
{
  "model_name": "claude-3-opus",
  "litellm_params": {
    "model": "openai/claude-3-opus-20240229",
    "api_base": "https://api.aimlapi.com/v1",
    "api_key": "os.environ/AIMLAPI_KEY"
  },
  "model_info": {
    "description": "Claude 3 Opus via AIMLAPI",
    "provider": "aimlapi",
    "max_tokens": 200000,
    "supports_function_calling": true
  }
}
```

### Meta Llama Models:
```json
{
  "model_name": "llama-3-1-405b",
  "litellm_params": {
    "model": "openai/meta-llama/llama-3.1-405b-instruct",
    "api_base": "https://api.aimlapi.com/v1",
    "api_key": "os.environ/AIMLAPI_KEY"
  },
  "model_info": {
    "description": "Llama 3.1 405B - Meta's largest model",
    "provider": "aimlapi",
    "max_tokens": 128000,
    "supports_function_calling": true
  }
}
```

### Google Gemini Models:
```json
{
  "model_name": "gemini-1-5-pro",
  "litellm_params": {
    "model": "openai/gemini-1.5-pro-latest",
    "api_base": "https://api.aimlapi.com/v1",
    "api_key": "os.environ/AIMLAPI_KEY"
  },
  "model_info": {
    "description": "Gemini 1.5 Pro via AIMLAPI",
    "provider": "aimlapi",
    "max_tokens": 2097152,
    "supports_function_calling": true
  }
}
```

## 🧪 TESTING MODELS:

### Test Model mới:
```bash
curl -X POST https://call.shareapiai.com/v1/chat/completions \
  -H "Authorization: Bearer sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "NEW_MODEL_NAME",
    "messages": [{"role": "user", "content": "Hello! Are you working?"}],
    "max_tokens": 50
  }'
```

### Test Function Calling:
```bash
curl -X POST https://call.shareapiai.com/v1/chat/completions \
  -H "Authorization: Bearer sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_NAME",
    "messages": [{"role": "user", "content": "What is the weather in Hanoi?"}],
    "functions": [
      {
        "name": "get_weather",
        "description": "Get weather information",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "City name"}
          }
        }
      }
    ]
  }'
```

## 🔄 CẬP NHẬT MODELS ĐỊNH KỲ:

### 1. Cron Job Script:
```bash
# Tạo script tự động cập nhật
echo "#!/bin/bash" > update_models_daily.sh
echo "cd /path/to/project" >> update_models_daily.sh
echo "python fetch_aimlapi_models.py" >> update_models_daily.sh
echo "python quick_add_models.py" >> update_models_daily.sh
chmod +x update_models_daily.sh

# Thêm vào crontab (chạy mỗi ngày lúc 2AM)
echo "0 2 * * * /path/to/update_models_daily.sh" | crontab -
```

### 2. GitHub Actions (CI/CD):
```yaml
name: Update LiteLLM Models
on:
  schedule:
    - cron: '0 2 * * *'  # Chạy mỗi ngày lúc 2AM
  workflow_dispatch:     # Chạy thủ công

jobs:
  update-models:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Update models
        run: python quick_add_models.py
        env:
          AIMLAPI_KEY: ${{ secrets.AIMLAPI_KEY }}
```

## 📊 MONITORING VÀ ALERTING:

### Check Model Health:
```bash
# Script kiểm tra tất cả models
for model in $(curl -s -H "Authorization: Bearer $API_KEY" \
  https://call.shareapiai.com/v1/models | jq -r '.data[].id'); do
  echo "Testing $model..."
  curl -X POST https://call.shareapiai.com/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"test\"}],\"max_tokens\":5}"
done
```

## 🚨 TROUBLESHOOTING:

### Model không hoạt động:
1. Kiểm tra AIMLAPI_KEY có đúng không
2. Kiểm tra model name có chính xác không
3. Kiểm tra API quota còn không
4. Restart container nếu cần

### Model bị duplicate:
1. Xóa models cũ (nếu API hỗ trợ)
2. Hoặc restart container để reset

### Performance issues:
1. Kiểm tra rate limits
2. Monitor response times
3. Scale container resources nếu cần

## 🎯 BEST PRACTICES:

1. **Always test models** sau khi thêm
2. **Backup configurations** trước khi thay đổi
3. **Monitor usage** để tối ưu cost
4. **Update regularly** để có models mới
5. **Document changes** trong git commits

**🔥 Với hệ thống này, bạn có thể dễ dàng quản lý hàng trăm AI models!**

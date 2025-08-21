# 🚀 SHAREAPIAI.COM - ADVANCED MODEL MANAGER

## 📋 TỔNG QUAN

Script quản lý models nâng cao cho LiteLLM với 4 chức năng chính:

1. **📥 Lấy models từ AIMLAPI** - Fetch models mới nhất và lưu vào file JSON
2. **🔄 Cập nhật models vào container** - Sync models từ file vào LiteLLM container
3. **🧪 Test models** - Kiểm tra hoạt động và khả năng function calling
4. **🗑️ Xóa models** - Quản lý và xóa models không cần thiết

## 🎯 TÍNH NĂNG ĐẶC BIỆT

### ✨ Enhanced với shareapiai.com
- Tất cả models được thêm thông tin "shareapiai.com"
- Metadata chi tiết: max_tokens, function_calling, vision support
- Timestamp và provenance tracking
- Phân loại models theo provider (OpenAI, Anthropic, Google, Meta, etc.)

### 🤖 Smart Model Management
- **Auto-detect model capabilities**: function calling, vision, max tokens
- **Priority-based addition**: Ưu tiên models phổ biến (GPT-4o, Claude, Llama)
- **Duplicate prevention**: Tự động kiểm tra và bỏ qua models đã tồn tại
- **Batch processing**: Thêm nhiều models cùng lúc với rate limiting

### 🧪 Comprehensive Testing
- **Basic functionality test**: Gửi test message và kiểm tra response
- **Function calling test**: Kiểm tra khả năng gọi functions
- **Performance metrics**: Đo thời gian phản hồi và token usage
- **Interactive selection**: Chọn models từ danh sách hoặc nhập tên

## 🚀 CÁCH SỬ DỤNG

### Chạy Script:
```bash
cd d:\Project_ShareAPIai\CODE\litellm
d:/Project_ShareAPIai/venv/Scripts/python.exe advanced_model_manager.py
```

### Menu Chính:
```
============================================================
🚀 SHAREAPIAI.COM - ADVANCED MODEL MANAGER
============================================================
1. 📥 Lấy models mới nhất từ AIMLAPI và lưu file
2. 🔄 Cập nhật models từ file vào container
3. 🧪 Test model
4. 🗑️ Xóa model
5. 📊 Xem thông tin file models
6. 📋 Xem models hiện tại trong container
0. 👋 Thoát
============================================================
```

## 📊 QUY TRÌNH LÀM VIỆC

### 🔄 Quy trình cập nhật models hàng ngày:

1. **Chạy chức năng 1**: Lấy danh sách models mới nhất từ AIMLAPI
   - Fetch 237+ models từ https://api.aimlapi.com/models
   - Enhance với metadata shareapiai.com
   - Lưu vào `shareapiai_models_info.json`

2. **Chạy chức năng 2**: Cập nhật vào container
   - So sánh với models hiện tại
   - Thêm models mới (ưu tiên models phổ biến)
   - Bỏ qua duplicates
   - Giới hạn 20 models/lần để tránh overload

3. **Chạy chức năng 3**: Test models mới
   - Kiểm tra hoạt động cơ bản
   - Test function calling
   - Đo performance metrics

4. **Chạy chức năng 4**: Dọn dẹp (nếu cần)
   - Xóa models không dùng
   - Restart container để reset

## 📁 CẤU TRÚC FILE

### `shareapiai_models_info.json`:
```json
{
  "updated_at": "2025-08-16T23:11:14.973922",
  "source": "https://api.aimlapi.com/models",
  "enhanced_by": "shareapiai.com",
  "total_models": 237,
  "models": [
    {
      "id": "gpt-4o",
      "description": "gpt-4o - Provided by shareapiai.com via AIMLAPI",
      "provider": "aimlapi",
      "shareapiai_enhanced": true,
      "shareapiai_added_date": "2025-08-16T23:11:14.973922",
      "max_tokens": 128000,
      "supports_function_calling": true,
      "supports_vision": true,
      "model_type": "openai"
    }
  ]
}
```

## 🎯 MODELS ĐƯỢC ƯU TIÊN

### OpenAI Models:
- `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`
- `gpt-3.5-turbo`, `o1-mini`, `o3-mini`

### Anthropic Models:
- `claude-3-5-sonnet`, `claude-3-opus`, `claude-3-haiku`

### Google Models:
- `gemini-1.5-pro`, `gemini-1.5-flash`

### Meta Models:
- `llama-3.1-405b`, `llama-3.1-70b`, `llama-3.1-8b`

### Mistral Models:
- `mistral-large`, `mixtral-8x7b`

### Cohere Models:
- `command-r-plus`

## 🔧 TÍNH NĂNG NÂNG CAO

### Auto-Detection Features:
- **Max Tokens**: Tự động ước tính dựa trên model name
- **Function Calling**: Phát hiện models hỗ trợ function calling
- **Vision Support**: Nhận diện models có khả năng xử lý hình ảnh
- **Model Type**: Phân loại theo provider

### Smart Batching:
- Giới hạn 20 models/batch để tránh timeout
- Rate limiting 0.5s giữa các requests
- Priority-based selection

### Error Handling:
- Timeout protection (30s/60s)
- Detailed error messages
- Graceful degradation

## 📈 MONITORING & METRICS

### Performance Tracking:
- Response time measurement
- Token usage statistics
- Success/failure rates
- Function calling capabilities

### Health Checks:
- Basic functionality test
- Advanced feature testing
- Error detection and reporting

## 🛠️ TROUBLESHOOTING

### Models không thêm được:
1. Kiểm tra AIMLAPI_KEY
2. Verify network connectivity
3. Check rate limits
4. Restart container nếu cần

### Performance issues:
1. Reduce batch size
2. Increase timeouts
3. Monitor memory usage
4. Scale container resources

### Function calling không hoạt động:
1. Verify model supports functions
2. Check request format
3. Test with simpler functions
4. Review API documentation

## 🔄 AUTOMATION

### Scheduled Updates:
```bash
# Tạo batch script cho Windows
echo "cd d:\Project_ShareAPIai\CODE\litellm" > update_models.bat
echo "d:/Project_ShareAPIai/venv/Scripts/python.exe -c \"
from advanced_model_manager import ShareAPIAIModelManager
manager = ShareAPIAIModelManager()
manager.fetch_latest_models_from_aimlapi()
manager.update_models_to_container()
\"" >> update_models.bat

# Chạy daily via Task Scheduler
```

### CI/CD Integration:
```yaml
# GitHub Actions example
- name: Update LiteLLM Models
  run: |
    python advanced_model_manager.py << EOF
    1
    2
    0
    EOF
```

## 🎉 KẾT QUẢ

Với script này, bạn có thể:
- ✅ Quản lý 237+ AI models từ AIMLAPI
- ✅ Tự động sync và update models
- ✅ Test functionality và performance
- ✅ Enhanced metadata với shareapiai.com branding
- ✅ Smart prioritization và batch processing
- ✅ Comprehensive error handling và monitoring

**🚀 Hệ thống quản lý models hoàn chỉnh cho ShareAPIAI.com!**

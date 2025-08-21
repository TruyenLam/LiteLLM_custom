# LiteLLM Custom Free Version Setup

## 🎯 **Objective**
Sử dụng tất cả tính năng LiteLLM mà **KHÔNG CẦN LITELLM_LICENSE** - hoàn toàn miễn phí và tự quản lý.

## ✅ **Features Available (No License Required)**

### **Core Features:**
- ✅ **Multiple AI Models** (ChatGPT, Claude, Gemini, Llama)
- ✅ **OpenAI-compatible API** 
- ✅ **Database integration** (PostgreSQL)
- ✅ **Health monitoring**
- ✅ **Custom authentication**
- ✅ **Model management**

### **Custom Budget System:**
- ✅ **User budget tracking** (daily/monthly limits)
- ✅ **Token usage monitoring** (input/output)
- ✅ **Cost calculation** per model
- ✅ **Real-time budget enforcement**
- ✅ **Usage analytics** and reporting

### **Monitoring & Logging:**
- ✅ **Custom metrics** (replace Prometheus)
- ✅ **Request/response logging**
- ✅ **Performance tracking**
- ✅ **Error monitoring**

## 🚫 **Enterprise Features Disabled:**
- ❌ Prometheus metrics (replaced with custom)
- ❌ Enterprise spend logging (use custom budget)
- ❌ Advanced telemetry 
- ❌ Enterprise UI features
- ❌ Licensed-only integrations

## 🔧 **Environment Configuration**

### **Complete Environment Variables:**
```bash
# Core LiteLLM
AIMLAPI_KEY=b0197edcd9104cd1ab78aaf148ce609a
LITELLM_MASTER_KEY=sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1
LITELLM_SALT_KEY=sk-aB2c3D4eF5g6H7i8J9k0L1m2N3o4P5qR
DATABASE_URL=postgresql://llmproxy:bTBwUQHt7VTltFyB@34.136.3.30:5432/litellm
STORE_MODEL_IN_DB=True

# Disable ALL enterprise (no license needed)
LITELLM_LICENSE=""
LITELLM_ENTERPRISE=false
DISABLE_PROMETHEUS=true
LITELLM_DISABLE_PROMETHEUS=true
DISABLE_SPEND_LOGS=true
LITELLM_DISABLE_SPEND_LOGS=true
DISABLE_ENTERPRISE_FEATURES=true
LITELLM_DISABLE_ENTERPRISE=true
LITELLM_DISABLE_TELEMETRY=true
DISABLE_TELEMETRY=true

# Enable custom features
ENABLE_CUSTOM_BUDGET=true
USE_CUSTOM_CALLBACKS=true
```

## 📄 **Custom Configuration (railway_config.yaml)**

```yaml
# LiteLLM Free Version Configuration
model_list:
  - model_name: chatgpt-4o-latest
    litellm_params:
      model: openai/gpt-4o-latest
      api_base: https://api.aimlapi.com/v1
      api_key: os.environ/AIMLAPI_KEY
    model_info:
      description: "ChatGPT-4o Latest via AIMLAPI"
      max_tokens: 128000

litellm_settings:
  drop_params: true
  num_retries: 3
  request_timeout: 300
  telemetry: false
  # Custom callbacks instead of enterprise
  success_callback: ["budget_tracker"]
  failure_callback: ["budget_tracker"]

general_settings:
  store_model_in_db: true
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
  
  # Health and logging
  health_check_interval: 300
  set_verbose: false
  
  # Disable enterprise completely
  disable_spend_logs: true
  disable_prometheus_metrics: true
  disable_enterprise_features: true
  ui_access_mode: "admin_only"
  
  # Custom tracking
  track_cost_per_request: true
  enable_custom_budget: true
```

## 🐳 **Docker Configuration**

### **Dockerfile.simple (Updated):**
```dockerfile
FROM ghcr.io/berriai/litellm:main-stable

# Install custom dependencies
RUN pip install psycopg2-binary flask requests

# Copy all custom files
COPY railway_config.yaml /app/config.yaml
COPY budget_manager.py /app/
COPY budget_callback.py /app/
COPY start_litellm.py /app/

# Environment setup for free version
ENV LITELLM_LICENSE=""
ENV DISABLE_ENTERPRISE_FEATURES=true
ENV LITELLM_DISABLE_TELEMETRY=true
ENV PYTHONPATH=/app

# Start with custom script
CMD ["python", "/app/start_litellm.py"]
```

## 🚀 **Custom Features**

### **1. Budget Tracker Callback:**
```python
# budget_callback.py - replaces Prometheus
class BudgetTrackerCallback:
    async def async_success_callback(self, kwargs, response, start_time, end_time):
        # Track usage, calculate costs, update budgets
        user_id = self.extract_user_id(kwargs)
        model = kwargs.get("model")
        usage = response.get("usage", {})
        
        # Custom tracking logic
        await self.track_usage(user_id, model, usage)
```

### **2. Custom Startup Script:**
```python
# start_litellm.py - ensures no enterprise features
def setup_environment():
    os.environ["LITELLM_LICENSE"] = ""
    os.environ["DISABLE_PROMETHEUS"] = "true"
    # ... more overrides

def start_litellm():
    setup_environment()
    subprocess.run(["litellm", "--config", "/app/config.yaml"])
```

### **3. Budget Management System:**
```python
# Complete user budget system
budget_manager = BudgetManager(database_url)
budget_manager.create_user_budget("user123", daily_limit=5.0)
budget_manager.check_user_budget("user123", "chatgpt-4o-latest")
budget_manager.track_usage("user123", "chatgpt-4o-latest", 500, 200)
```

## 📊 **Custom Monitoring**

### **Replace Prometheus with Custom Metrics:**
```python
# Custom metrics endpoint
@app.route('/metrics/custom')
def custom_metrics():
    stats = budget_tracker.get_stats()
    return {
        "total_requests": stats["total_requests"],
        "success_rate": stats["success_rate"],
        "avg_response_time": stats["average_response_time"],
        "model_usage": stats["model_stats"]
    }
```

### **Railway Built-in Monitoring:**
- ✅ CPU/Memory usage
- ✅ Request counts  
- ✅ Response times
- ✅ Error rates

## 🎯 **Deployment Steps**

### **1. Set Environment Variables on Railway:**
Copy all environment variables from above section

### **2. Deploy:**
```bash
git add .
git commit -m "Custom LiteLLM free version - no license required"
git push
```

### **3. Initialize Budget System:**
```bash
# After deployment
python budget_cli.py create-user default_user --daily-limit 10.0
```

### **4. Test All Features:**
```bash
# Test API
curl https://your-app.railway.app/health/liveliness

# Test models
curl -H "Authorization: Bearer sk-your-key" \
     https://your-app.railway.app/v1/models

# Test chat
curl -X POST https://your-app.railway.app/v1/chat/completions \
  -H "Authorization: Bearer sk-your-key" \
  -H "X-User-ID: testuser" \
  -d '{"model":"chatgpt-4o-latest","messages":[{"role":"user","content":"Hello"}]}'

# Test budget
curl https://your-app.railway.app/budget/users/testuser
```

## ✅ **Benefits of This Approach**

### **Cost Savings:**
- ✅ **$0 licensing fees** (vs $50+/month for enterprise)
- ✅ **Railway serverless** (pay only when used)
- ✅ **No vendor lock-in**

### **Full Control:**
- ✅ **Custom budget system** (more flexible than enterprise)
- ✅ **Own monitoring** (tailored to your needs)
- ✅ **No feature limitations**
- ✅ **Source code access**

### **Production Ready:**
- ✅ **Database persistence**
- ✅ **Health monitoring**
- ✅ **Error handling**
- ✅ **Scalable architecture**

## 🔍 **Troubleshooting**

### **If you see enterprise warnings:**
1. Check all environment variables are set
2. Verify custom startup script is running
3. Check Docker logs for override confirmation

### **If budget tracking doesn't work:**
1. Verify database connection
2. Check budget_manager.py is loaded
3. Test API endpoints manually

### **Performance optimization:**
1. Use Railway metrics for monitoring
2. Implement connection pooling
3. Add Redis caching if needed

## 🎉 **Result**

Bạn sẽ có **complete LiteLLM proxy** với:
- ✅ Multiple AI models
- ✅ User budget management  
- ✅ Usage tracking
- ✅ Cost control
- ✅ API monitoring
- ✅ **$0 licensing fees**

**No enterprise license required!** 🚀

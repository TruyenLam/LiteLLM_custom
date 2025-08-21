# Basic LiteLLM Monitoring (Free Alternative)

## 🆓 **Free Monitoring Solutions:**

### **1. Database Queries (Usage Tracking):**
```sql
-- Query LiteLLM database for usage stats
SELECT 
    model,
    COUNT(*) as requests,
    AVG(response_time_ms) as avg_response_time,
    DATE(created_at) as date
FROM LiteLLM_RequestTable 
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY model, DATE(created_at)
ORDER BY date DESC;
```

### **2. Railway Built-in Metrics:**
Railway Dashboard provides:
- ✅ **CPU Usage**
- ✅ **Memory Usage** 
- ✅ **Request Count**
- ✅ **Response Times**
- ✅ **Error Rates**

### **3. Custom Logging Script:**
```python
import requests
import time
import json
from datetime import datetime

def monitor_litellm():
    endpoint = "https://your-app.railway.app"
    headers = {"Authorization": "Bearer sk-your-master-key"}
    
    # Test request với token counting
    response = requests.post(f"{endpoint}/v1/chat/completions", 
        headers=headers,
        json={
            "model": "chatgpt-4o-latest",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 100
        }
    )
    
    # Log usage
    print(f"{datetime.now()}: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        usage = data.get('usage', {})
        print(f"Input tokens: {usage.get('prompt_tokens', 0)}")
        print(f"Output tokens: {usage.get('completion_tokens', 0)}")
        print(f"Total tokens: {usage.get('total_tokens', 0)}")

# Run monitoring
monitor_litellm()
```

### **4. Simple Budget Control:**
```python
# Simple budget tracking script
import requests
import json

class SimpleBudgetTracker:
    def __init__(self, daily_limit_usd=10):
        self.daily_limit = daily_limit_usd
        self.usage_file = "daily_usage.json"
    
    def track_request(self, model, input_tokens, output_tokens):
        # Estimate costs (rough)
        costs = {
            "chatgpt-4o-latest": {"input": 0.005/1000, "output": 0.015/1000},
            "claude-3-5-sonnet": {"input": 0.003/1000, "output": 0.015/1000}
        }
        
        if model in costs:
            cost = (input_tokens * costs[model]["input"] + 
                   output_tokens * costs[model]["output"])
            
            # Load current usage
            try:
                with open(self.usage_file, 'r') as f:
                    usage = json.load(f)
            except:
                usage = {"date": str(datetime.now().date()), "cost": 0}
            
            # Reset if new day
            if usage["date"] != str(datetime.now().date()):
                usage = {"date": str(datetime.now().date()), "cost": 0}
            
            # Add cost
            usage["cost"] += cost
            
            # Check limit
            if usage["cost"] > self.daily_limit:
                print(f"⚠️ Budget exceeded! ${usage['cost']:.4f} > ${self.daily_limit}")
                return False
            
            # Save usage
            with open(self.usage_file, 'w') as f:
                json.dump(usage, f)
            
            print(f"✅ Cost: ${cost:.4f}, Daily total: ${usage['cost']:.4f}")
            return True
        
        return True
```

## 🚀 **Recommendations:**

### **Option 1: Keep Prometheus Disabled (Recommended cho dev)**
- ✅ Clean startup, no warnings
- ✅ Full functionality
- ✅ Use Railway metrics + custom monitoring
- ✅ Free solution

### **Option 2: Get LiteLLM Enterprise Trial**
- Get 7-day trial: https://www.litellm.ai/enterprise#trial
- Full Prometheus metrics
- Advanced budget controls
- Team management features

### **Option 3: Hybrid Approach**
- Keep LiteLLM free
- Use external monitoring (Grafana, Datadog)
- Custom budget tracking scripts
- Railway built-in metrics

## 📋 **Quick Decision Matrix:**

| Feature | Free (No Prometheus) | Enterprise |
|---------|---------------------|------------|
| Core API | ✅ | ✅ |
| Token Usage | Basic logging | Detailed metrics |
| Budget Control | Manual/Custom | Built-in |
| Real-time Monitoring | Railway Dashboard | Prometheus + Grafana |
| Cost | $0 | $50+/month |
| Setup Complexity | Low | Medium |

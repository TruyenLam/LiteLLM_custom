# User Budget Management System

## 🎯 **Overview**

Hệ thống quản lý ngân sách người dùng cho LiteLLM, theo dõi input/output tokens và áp dụng giới hạn chi tiêu theo ngày/tháng.

## 🚀 **Features**

### ✅ **Core Features:**
- **Per-user budget limits** (daily & monthly)
- **Real-time token tracking** (input + output)
- **Cost calculation** based on actual model pricing
- **Budget enforcement** (block requests when exceeded)
- **Usage analytics** and reporting
- **REST API** for budget management
- **CLI tools** for administration

### 💰 **Model Pricing (per 1K tokens):**
```python
{
    "chatgpt-4o-latest": {"input": $0.005, "output": $0.015},
    "chatgpt-4o": {"input": $0.005, "output": $0.015},
    "chatgpt-4o-mini": {"input": $0.00015, "output": $0.0006},
    "claude-3-5-sonnet": {"input": $0.003, "output": $0.015},
    "gemini-1-5-pro": {"input": $0.00125, "output": $0.005},
    "llama-3-1-70b": {"input": $0.0009, "output": $0.0009},
    "llama-3-1-8b": {"input": $0.0002, "output": $0.0002}
}
```

## 📋 **Database Schema**

### **user_budgets table:**
```sql
CREATE TABLE user_budgets (
    user_id VARCHAR(255) PRIMARY KEY,
    daily_limit_usd DECIMAL(10,4) DEFAULT 10.0,
    monthly_limit_usd DECIMAL(10,4) DEFAULT 100.0,
    current_daily_spend DECIMAL(10,4) DEFAULT 0.0,
    current_monthly_spend DECIMAL(10,4) DEFAULT 0.0,
    total_tokens_input BIGINT DEFAULT 0,
    total_tokens_output BIGINT DEFAULT 0,
    last_reset_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **user_usage_logs table:**
```sql
CREATE TABLE user_usage_logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    model VARCHAR(100),
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd DECIMAL(10,6),
    request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 **CLI Usage**

### **Setup Database:**
```bash
python budget_cli.py create-user user123 --daily-limit 5.0 --monthly-limit 50.0
```

### **Check User Budget:**
```bash
python budget_cli.py check user123 --model chatgpt-4o-latest --tokens 1000
```

### **Get User Statistics:**
```bash
python budget_cli.py stats user123
```

### **Track Usage (manual):**
```bash
python budget_cli.py track user123 chatgpt-4o-latest 500 200
```

## 🌐 **REST API**

### **Create User Budget:**
```bash
curl -X POST https://your-app.railway.app/budget/users \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "daily_limit": 5.0,
    "monthly_limit": 50.0
  }'
```

### **Check Budget:**
```bash
curl -X POST https://your-app.railway.app/budget/users/user123/check \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chatgpt-4o-latest",
    "estimated_tokens": 1000
  }'
```

### **Get User Stats:**
```bash
curl https://your-app.railway.app/budget/users/user123
```

### **Track Usage:**
```bash
curl -X POST https://your-app.railway.app/budget/users/user123/usage \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chatgpt-4o-latest",
    "input_tokens": 500,
    "output_tokens": 200
  }'
```

## 🔄 **Integration with LiteLLM**

### **Automatic Budget Checking:**
Budget middleware automatically:
1. **Pre-request**: Check user budget before processing
2. **Post-request**: Track actual usage and update budget
3. **Block requests** if budget exceeded
4. **Add budget info** to response

### **User Identification:**
```bash
# Option 1: Custom header
curl -X POST https://your-app.railway.app/v1/chat/completions \
  -H "Authorization: Bearer sk-your-master-key" \
  -H "X-User-ID: user123" \
  -H "Content-Type: application/json" \
  -d '{"model": "chatgpt-4o-latest", "messages": [...]}'

# Option 2: Custom API key (user-specific)
curl -X POST https://your-app.railway.app/v1/chat/completions \
  -H "Authorization: Bearer sk-user123-custom-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "chatgpt-4o-latest", "messages": [...]}'
```

### **Response with Budget Info:**
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "model": "chatgpt-4o-latest",
  "choices": [...],
  "usage": {
    "prompt_tokens": 500,
    "completion_tokens": 200,
    "total_tokens": 700
  },
  "budget_info": {
    "user_id": "user123",
    "cost": 0.0055,
    "daily_remaining": 4.9945,
    "monthly_remaining": 49.9945
  }
}
```

## 🚨 **Budget Exceeded Response:**
```json
{
  "error": {
    "type": "budget_exceeded",
    "message": "Daily budget exceeded: $5.0012 + $0.0055 > $5.00",
    "code": "BUDGET_EXCEEDED",
    "details": {
      "daily_remaining": -0.0012,
      "monthly_remaining": 45.23,
      "estimated_cost": 0.0055
    }
  }
}
```

## 📊 **Usage Analytics**

### **User Statistics Response:**
```json
{
  "user_id": "user123",
  "budget": {
    "daily_limit": 5.0,
    "monthly_limit": 50.0,
    "daily_spent": 2.45,
    "monthly_spent": 15.67,
    "daily_remaining": 2.55,
    "monthly_remaining": 34.33
  },
  "usage": {
    "total_input_tokens": 45000,
    "total_output_tokens": 18000,
    "total_tokens": 63000
  },
  "recent_models": [
    {
      "model": "chatgpt-4o-latest",
      "input_tokens": 15000,
      "output_tokens": 6000,
      "cost": 1.165,
      "requests": 25
    }
  ]
}
```

## 🔒 **Security & Best Practices**

### **Environment Variables:**
```bash
DATABASE_URL=postgresql://user:pass@host:port/db
LITELLM_MASTER_KEY=sk-your-master-key
BUDGET_API_SECRET=your-budget-api-secret  # Optional
```

### **Rate Limiting:**
- Consider adding rate limiting per user
- Implement IP-based protection
- Use Redis for distributed rate limiting

### **Database Security:**
- Use connection pooling
- Implement read replicas for analytics
- Regular backups of budget data

## 🚀 **Deployment Steps**

### **1. Update Railway Environment:**
```bash
# Add to Railway environment variables
DATABASE_URL=postgresql://your-db-url
LITELLM_MASTER_KEY=sk-your-key
LITELLM_SALT_KEY=sk-your-salt-key
AIMLAPI_KEY=your-aimlapi-key
```

### **2. Deploy with Budget System:**
```bash
git add .
git commit -m "Add user budget management system"
git push
```

### **3. Initialize Database:**
```bash
# After deployment, run once to create tables
python budget_manager.py
```

### **4. Create Test Users:**
```bash
python budget_cli.py create-user testuser --daily-limit 1.0 --monthly-limit 10.0
```

## 📈 **Monitoring & Alerts**

### **Database Queries for Monitoring:**
```sql
-- Daily spending by user
SELECT user_id, current_daily_spend, daily_limit_usd
FROM user_budgets 
WHERE current_daily_spend > daily_limit_usd * 0.8
ORDER BY current_daily_spend DESC;

-- Top users by usage
SELECT user_id, total_tokens_input + total_tokens_output as total_tokens
FROM user_budgets 
ORDER BY total_tokens DESC LIMIT 10;

-- Usage by model (last 7 days)
SELECT model, SUM(cost_usd), COUNT(*)
FROM user_usage_logs 
WHERE request_timestamp >= NOW() - INTERVAL '7 days'
GROUP BY model
ORDER BY SUM(cost_usd) DESC;
```

## 🎯 **Next Steps**

- **Implement alerts** when users approach limits
- **Add webhook notifications** for budget events
- **Create admin dashboard** for budget management
- **Implement team/organization budgets**
- **Add prepaid credit system**

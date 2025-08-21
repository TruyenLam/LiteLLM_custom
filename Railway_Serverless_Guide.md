# Railway Serverless Configuration Guide

## 🚀 **Serverless Mode Overview**

Railway Serverless cho phép:
- ✅ **Scale to Zero**: Container sẽ sleep khi không có traffic
- ✅ **Auto Scale Up**: Tự động wake up khi có requests
- ✅ **Cost Optimization**: Chỉ trả tiền khi container đang chạy
- ✅ **Queue Requests**: Requests sẽ được queue trong khi container wake up

## 🔧 **Configuration**

### **railway.json đã được cập nhật:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.simple"
  },
  "deploy": {
    "sleepApplication": true,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### **Key Changes:**
- ❌ Removed `numReplicas: 1` (serverless auto-manages replicas)
- ✅ Set `sleepApplication: true` (enables scale-to-zero)
- ✅ Keeps restart policy for reliability

## 📋 **Environment Variables (Không đổi)**

Serverless vẫn cần các environment variables như trước:
```bash
AIMLAPI_KEY=b0197edcd9104cd1ab78aaf148ce609a
LITELLM_MASTER_KEY=sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1
LITELLM_SALT_KEY=sk-aB2c3D4eF5g6H7i8J9k0L1m2N3o4P5qR
DATABASE_URL=postgresql://llmproxy:bTBwUQHt7VTltFyB@34.136.3.30:5432/litellm
STORE_MODEL_IN_DB=True
```

## ⚡ **Serverless Behavior**

### **Cold Start:**
- First request sau khi sleep: ~10-30 seconds để wake up
- Subsequent requests: Instant response

### **Sleep Timer:**
- Container sleep sau ~15 minutes không có traffic
- Health checks không prevent sleep

### **Wake Up Process:**
```
Request → Queue → Container Wake → Health Check → Process Request → Response
```

## 🚀 **Deployment Steps**

### **1. Push Updated Config:**
```bash
git add railway.json
git commit -m "Enable Railway Serverless mode"
git push
```

### **2. Enable trên Railway Dashboard:**
- Vào Project Settings → General
- Tìm "Serverless" section
- Toggle "Enable Serverless" = ON
- Railway sẽ tự động redeploy

### **3. Verify Serverless:**
```bash
# Test immediate response (if container is awake)
curl https://your-app.railway.app/health/liveliness

# Test after sleep period (will trigger cold start)
# Wait 20+ minutes, then test again
curl https://your-app.railway.app/v1/models \
  -H "Authorization: Bearer sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1"
```

## 💰 **Cost Benefits**

### **Before (Always On):**
- 24/7 container running
- Full memory/CPU usage charged

### **After (Serverless):**
- Only charged when processing requests
- ~70-90% cost reduction for low-traffic apps
- Perfect cho development/testing

## ⚠️ **Considerations**

### **Pros:**
- ✅ Massive cost savings
- ✅ Auto-scaling
- ✅ Zero maintenance

### **Cons:**
- ❌ Cold start latency (10-30s)
- ❌ Not suitable for real-time applications
- ❌ Database connections may timeout

### **Best For:**
- 🎯 Development/Testing environments
- 🎯 Low-traffic applications
- 🎯 Batch processing
- 🎯 Cost-sensitive deployments

## 🔧 **Troubleshooting**

### **If container won't sleep:**
- Check for persistent connections
- Verify no background jobs running
- Review health check frequency

### **If cold starts are too slow:**
- Consider using Railway's "Always On" mode
- Optimize Dockerfile for faster startup
- Use smaller base images

### **Database Connection Issues:**
- Use connection pooling
- Implement connection retry logic
- Consider PostgreSQL connection limits

## 📊 **Monitoring**

### **Railway Dashboard:**
- Monitor sleep/wake cycles
- Track cold start times
- Review cost savings

### **Health Monitoring:**
```bash
# Setup monitoring endpoint
curl https://your-app.railway.app/health/readiness

# Monitor response times
time curl https://your-app.railway.app/v1/models
```

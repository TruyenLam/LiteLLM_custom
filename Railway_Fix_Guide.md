# Railway Deployment Fix Guide

## Lỗi và Giải pháp

### Lỗi hiện tại:
```
Error: Got unexpected extra argument (litellm)
```

### Nguyên nhân:
- Base image `ghcr.io/berriai/litellm:main-stable` đã có entry point sẵn
- Không cần gọi `litellm` command trong CMD

### Giải pháp:

#### Option 1: Sử dụng Dockerfile.simple (Khuyến nghị)
```dockerfile
FROM ghcr.io/berriai/litellm:main-stable
COPY railway_config.yaml /app/config.yaml
ENV PORT=4000
CMD ["--config", "/app/config.yaml"]
```

#### Option 2: Sử dụng Dockerfile.alt (Backup)
```dockerfile
FROM python:3.11-slim
RUN pip install litellm[proxy]
COPY railway_config.yaml /app/config.yaml
CMD ["litellm", "--config", "/app/config.yaml", "--port", "4000", "--host", "0.0.0.0"]
```

## Các bước triển khai:

### 1. Push code mới lên GitHub:
```bash
git add .
git commit -m "Fix Railway Dockerfile command"
git push
```

### 2. Triển khai trên Railway:
- Vào Railway Dashboard
- Redeploy từ GitHub
- Railway sẽ tự động detect `railway.json` và sử dụng `Dockerfile.simple`

### 3. Set Environment Variables trên Railway:
```
# Core configuration
AIMLAPI_KEY=b0197edcd9104cd1ab78aaf148ce609a
LITELLM_MASTER_KEY=sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1
LITELLM_SALT_KEY=sk-aB2c3D4eF5g6H7i8J9k0L1m2N3o4P5qR
DATABASE_URL=postgresql://llmproxy:bTBwUQHt7VTltFyB@34.136.3.30:5432/litellm
STORE_MODEL_IN_DB=True

# Disable ALL enterprise features (no license needed)
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

### 4. Test deployment:
```bash
curl https://your-app.railway.app/health/liveliness
curl -H "Authorization: Bearer sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1" \
     https://your-app.railway.app/v1/models
```

## Nếu vẫn lỗi:

### Thử đổi railway.json sang Dockerfile.alt:
```json
{
  "build": {
    "dockerfilePath": "Dockerfile.alt"
  }
}
```

### Hoặc không dùng railway.json, để Railway auto-detect:
- Đổi tên `Dockerfile.simple` thành `Dockerfile`
- Xóa `railway.json`

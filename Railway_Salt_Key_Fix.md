# LiteLLM Salt Key Fix for Railway

## 🚨 **Lỗi Salt Key Decryption**

### **Lỗi bạn đang gặp:**
```
Error: Decryption failed. Ciphertext failed verification
Error decrypting value for key: api_base, Did your master_key/salt key change recently?
```

### **Nguyên nhân:**
- LiteLLM sử dụng `LITELLM_SALT_KEY` để mã hóa/giải mã dữ liệu nhạy cảm trong database
- Khi deploy lên Railway mà không có salt key cố định, LiteLLM không thể decrypt dữ liệu đã mã hóa
- Database PostgreSQL chứa dữ liệu đã được mã hóa bằng salt key từ local environment

## 🔧 **Giải pháp:**

### **Option 1: Sử dụng cùng Salt Key (Khuyến nghị)**

Trên Railway Dashboard, thêm environment variable:
```
LITELLM_SALT_KEY=sk-aB2c3D4eF5g6H7i8J9k0L1m2N3o4P5qR
```

### **Option 2: Reset Database (Nếu Option 1 không work)**

Nếu vẫn lỗi, có thể cần clear encrypted data trong database:

1. **Connect vào database:**
```sql
-- Clear encrypted model configs
DELETE FROM LiteLLM_ProxyModelTable;

-- Clear encrypted keys
DELETE FROM LiteLLM_KeyTable WHERE encrypted = true;
```

2. **Hoặc recreate tables:**
```sql
-- Drop và recreate tables
DROP TABLE IF EXISTS LiteLLM_ProxyModelTable CASCADE;
DROP TABLE IF EXISTS LiteLLM_KeyTable CASCADE;
```

### **Option 3: Fresh Database**

Tạo database mới cho Railway environment:
```
# New database URL cho Railway
DATABASE_URL=postgresql://new_user:new_pass@new_host:5432/new_db
```

## 📋 **Environment Variables cần thiết cho Railway:**

```bash
# Core LiteLLM
LITELLM_MASTER_KEY=sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1
LITELLM_SALT_KEY=sk-aB2c3D4eF5g6H7i8J9k0L1m2N3o4P5qR

# Database
DATABASE_URL=postgresql://llmproxy:bTBwUQHt7VTltFyB@34.136.3.30:5432/litellm
STORE_MODEL_IN_DB=True

# AI Provider
AIMLAPI_KEY=b0197edcd9104cd1ab78aaf148ce609a
```

## 🚀 **Deployment Steps:**

### 1. **Set Environment Variables trên Railway:**
- Vào Railway Dashboard → Project Settings → Environment
- Add tất cả các variables ở trên
- **Đặc biệt quan trọng: `LITELLM_SALT_KEY`**

### 2. **Redeploy:**
```bash
# Trigger redeploy from GitHub
git commit --allow-empty -m "Trigger Railway redeploy with salt key"
git push
```

### 3. **Verify:**
```bash
# Check health
curl https://your-app.railway.app/health/liveliness

# Check models 
curl -H "Authorization: Bearer sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1" \
     https://your-app.railway.app/v1/models
```

## 🔒 **Security Notes:**

- `LITELLM_SALT_KEY` phải giống nhau giữa các environments để decrypt được dữ liệu
- Key này dùng để mã hóa API keys và sensitive data trong database
- Không nên thay đổi salt key sau khi đã có dữ liệu trong database
- Sử dụng strong random key, ít nhất 32 characters

## 🆘 **Nếu vẫn lỗi:**

### Debug steps:
1. Check Railway logs để xem exact error
2. Verify all environment variables đã được set
3. Test với fresh database
4. Contact nếu cần recreate database tables

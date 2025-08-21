#!/bin/bash
# Script to initialize GitHub repo for LiteLLM_custom

echo "🚀 Khởi tạo GitHub repository cho LiteLLM_custom..."

# Kiểm tra git đã được khởi tạo chưa
if [ ! -d ".git" ]; then
    echo "📝 Khởi tạo Git repository..."
    git init
    git branch -M main
else
    echo "✅ Git repository đã tồn tại"
fi

# Add files to git
echo "📦 Thêm files vào Git..."
git add .
git commit -m "Initial commit: LiteLLM with AIMLAPI integration for Railway deployment

Features:
- AIMLAPI integration với 8+ AI models
- Railway-optimized Dockerfile
- PostgreSQL database persistence  
- Health checks và monitoring
- Environment configuration
- Documentation đầy đủ

Ready for Railway deployment! 🚀"

echo "
🎉 Git repository đã được khởi tạo!

📋 BƯỚC TIẾP THEO:

1. Tạo GitHub repository:
   - Đi tới https://github.com/new
   - Repository name: LiteLLM_custom
   - Visibility: Public hoặc Private
   - Không khởi tạo với README (đã có sẵn)

2. Kết nối với GitHub:
   git remote add origin https://github.com/YOUR_USERNAME/LiteLLM_custom.git
   git push -u origin main

3. Deploy trên Railway:
   - Đi tới https://railway.app
   - New Project → Deploy from GitHub repo
   - Chọn LiteLLM_custom repository
   - Thêm environment variables:
     * AIMLAPI_KEY=your_key
     * LITELLM_MASTER_KEY=your_master_key  
     * DATABASE_URL=postgresql_url

4. Test deployment:
   curl https://your-domain.railway.app/health/liveliness

🔗 Useful links:
- Railway Dashboard: https://railway.app/dashboard
- LiteLLM Docs: https://docs.litellm.ai/
- AIMLAPI: https://aimlapi.com/
"

# PowerShell script to initialize GitHub repo for LiteLLM_custom

Write-Host "🚀 Initializing GitHub repository for LiteLLM_custom..." -ForegroundColor Green

# Check if git is already initialized
if (-not (Test-Path ".git")) {
    Write-Host "📝 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Add files to git
Write-Host "📦 Adding files to Git..." -ForegroundColor Yellow
git add .
git commit -m "Initial commit: LiteLLM with AIMLAPI integration for Railway deployment

Features:
- AIMLAPI integration with 8+ AI models
- Railway-optimized Dockerfile
- PostgreSQL database persistence  
- Health checks and monitoring
- Environment configuration
- Complete documentation

Ready for Railway deployment! 🚀"

Write-Host ""
Write-Host "🎉 Git repository has been initialized!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create GitHub repository:" -ForegroundColor Cyan
Write-Host "   - Go to https://github.com/new"
Write-Host "   - Repository name: LiteLLM_custom"
Write-Host "   - Visibility: Public or Private"
Write-Host "   - Do NOT initialize with README (already exists)"
Write-Host ""
Write-Host "2. Connect to GitHub:" -ForegroundColor Cyan
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/LiteLLM_custom.git"
Write-Host "   git push -u origin main"
Write-Host ""
Write-Host "3. Deploy on Railway:" -ForegroundColor Cyan
Write-Host "   - Go to https://railway.app"
Write-Host "   - New Project → Deploy from GitHub repo"
Write-Host "   - Select LiteLLM_custom repository"
Write-Host "   - Add environment variables:"
Write-Host "     * AIMLAPI_KEY=your_key"
Write-Host "     * LITELLM_MASTER_KEY=your_master_key"
Write-Host "     * DATABASE_URL=postgresql_url"
Write-Host ""
Write-Host "4. Test deployment:" -ForegroundColor Cyan
Write-Host "   curl https://your-domain.railway.app/health/liveliness"
Write-Host ""
Write-Host "🔗 Useful links:" -ForegroundColor Yellow
Write-Host "- Railway Dashboard: https://railway.app/dashboard"
Write-Host "- LiteLLM Docs: https://docs.litellm.ai/"
Write-Host "- AIMLAPI: https://aimlapi.com/"
Write-Host ""
Write-Host "💡 To run next commands, copy and run:" -ForegroundColor Yellow
Write-Host "git remote add origin https://github.com/YOUR_USERNAME/LiteLLM_custom.git" -ForegroundColor White
Write-Host "git push -u origin main" -ForegroundColor White

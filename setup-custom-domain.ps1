# Script cấu hình Custom Domain cho LiteLLM App
# Chạy script này SAU KHI đã cấu hình DNS trên Hostinger

Write-Host "=== CẤU HÌNH CUSTOM DOMAIN CHO LITELLM-APP ===" -ForegroundColor Green
Write-Host ""

# Step 1: Check DNS first
Write-Host "Bước 1: Kiểm tra DNS..." -ForegroundColor Yellow
$dnsReady = $true

try {
    $aRecord = Resolve-DnsName -Name "call.shareapiai.com" -Type A -ErrorAction Stop
    if ($aRecord.IPAddress -eq "52.230.60.250") {
        Write-Host "✅ A Record OK: $($aRecord.IPAddress)" -ForegroundColor Green
    } else {
        Write-Host "❌ A Record sai IP: $($aRecord.IPAddress)" -ForegroundColor Red
        $dnsReady = $false
    }
} catch {
    Write-Host "❌ A Record chưa có" -ForegroundColor Red
    $dnsReady = $false
}

try {
    $txtRecord = Resolve-DnsName -Name "asuid.call.shareapiai.com" -Type TXT -ErrorAction Stop
    $expectedTxt = "664F5BF931382C5EF3D5F87B9514F5039B9E248A125642745034E5F34BC8CB01"
    if ($txtRecord.Strings -contains $expectedTxt) {
        Write-Host "✅ TXT Record OK" -ForegroundColor Green
    } else {
        Write-Host "❌ TXT Record sai" -ForegroundColor Red
        $dnsReady = $false
    }
} catch {
    Write-Host "❌ TXT Record chưa có" -ForegroundColor Red
    $dnsReady = $false
}

if (-not $dnsReady) {
    Write-Host ""
    Write-Host "⚠️  DNS chưa sẵn sàng. Vui lòng:" -ForegroundColor Red
    Write-Host "1. Đăng nhập Hostinger hPanel" -ForegroundColor Yellow
    Write-Host "2. Thêm A Record: call -> 52.230.60.250" -ForegroundColor Yellow
    Write-Host "3. Thêm TXT Record: asuid.call -> 664F5BF931382C5EF3D5F87B9514F5039B9E248A125642745034E5F34BC8CB01" -ForegroundColor Yellow
    Write-Host "4. Chờ 30-60 phút và chạy lại script này" -ForegroundColor Yellow
    return
}

# Step 2: Add hostname to container app
Write-Host ""
Write-Host "Bước 2: Thêm hostname vào Container App..." -ForegroundColor Yellow
try {
    az containerapp hostname add --name litellm-app --resource-group rg-litellm --hostname call.shareapiai.com
    Write-Host "✅ Hostname đã được thêm" -ForegroundColor Green
} catch {
    Write-Host "❌ Lỗi khi thêm hostname: $($_.Exception.Message)" -ForegroundColor Red
    return
}

# Step 3: Create managed certificate
Write-Host ""
Write-Host "Bước 3: Tạo SSL Certificate..." -ForegroundColor Yellow
try {
    az containerapp env certificate create --name litellm-env --resource-group rg-litellm --certificate-name shareapiai-cert --hostname call.shareapiai.com --validation-method HTTP
    Write-Host "✅ Certificate đã được tạo" -ForegroundColor Green
} catch {
    Write-Host "❌ Lỗi khi tạo certificate: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 4: Bind certificate to hostname
Write-Host ""
Write-Host "Bước 4: Bind Certificate..." -ForegroundColor Yellow
try {
    az containerapp hostname bind --name litellm-app --resource-group rg-litellm --hostname call.shareapiai.com --environment litellm-env
    Write-Host "✅ Certificate đã được bind" -ForegroundColor Green
} catch {
    Write-Host "❌ Lỗi khi bind certificate: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 5: Verify configuration
Write-Host ""
Write-Host "Bước 5: Kiểm tra cấu hình..." -ForegroundColor Yellow
az containerapp show --name litellm-app --resource-group rg-litellm --query "properties.configuration.ingress.customDomains"

Write-Host ""
Write-Host "🎉 HOÀN THÀNH! Bạn có thể truy cập:" -ForegroundColor Green
Write-Host "HTTP:  http://call.shareapiai.com" -ForegroundColor Cyan
Write-Host "HTTPS: https://call.shareapiai.com" -ForegroundColor Cyan
Write-Host "API:   https://call.shareapiai.com/health/liveliness" -ForegroundColor Cyan

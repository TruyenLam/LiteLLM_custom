# DNS Verification Script
# Chạy script này sau khi đã cấu hình DNS trên Hostinger

Write-Host "=== KIỂM TRA DNS CONFIGURATION ===" -ForegroundColor Green
Write-Host ""

# Check A record
Write-Host "1. Kiểm tra A Record cho call.shareapiai.com:" -ForegroundColor Yellow
try {
    $aRecord = Resolve-DnsName -Name "call.shareapiai.com" -Type A -ErrorAction Stop
    Write-Host "✅ A Record tìm thấy: $($aRecord.IPAddress)" -ForegroundColor Green
    if ($aRecord.IPAddress -eq "52.230.60.250") {
        Write-Host "✅ IP chính xác!" -ForegroundColor Green
    } else {
        Write-Host "❌ IP không đúng. Mong đợi: 52.230.60.250, Nhận được: $($aRecord.IPAddress)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Không tìm thấy A Record. DNS chưa propagate hoặc chưa cấu hình." -ForegroundColor Red
}

Write-Host ""

# Check TXT record
Write-Host "2. Kiểm tra TXT Record cho asuid.call.shareapiai.com:" -ForegroundColor Yellow
try {
    $txtRecord = Resolve-DnsName -Name "asuid.call.shareapiai.com" -Type TXT -ErrorAction Stop
    $expectedTxt = "664F5BF931382C5EF3D5F87B9514F5039B9E248A125642745034E5F34BC8CB01"
    Write-Host "✅ TXT Record tìm thấy: $($txtRecord.Strings)" -ForegroundColor Green
    if ($txtRecord.Strings -contains $expectedTxt) {
        Write-Host "✅ TXT Record chính xác!" -ForegroundColor Green
    } else {
        Write-Host "❌ TXT Record không đúng." -ForegroundColor Red
        Write-Host "Mong đợi: $expectedTxt" -ForegroundColor Yellow
        Write-Host "Nhận được: $($txtRecord.Strings)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Không tìm thấy TXT Record. DNS chưa propagate hoặc chưa cấu hình." -ForegroundColor Red
}

Write-Host ""
Write-Host "=== HƯỚNG DẪN TIẾP THEO ===" -ForegroundColor Cyan
Write-Host "Nếu cả 2 records đều OK, chạy lệnh sau để cấu hình Azure:" -ForegroundColor White
Write-Host ""
Write-Host "az containerapp hostname add --name litellm-app --resource-group rg-litellm --hostname call.shareapiai.com" -ForegroundColor Magenta
Write-Host ""
Write-Host "Nếu DNS chưa OK, chờ thêm 30-60 phút và chạy lại script này." -ForegroundColor Yellow

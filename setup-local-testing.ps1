# Local Testing với Hosts File (CHỈ ĐỂ TEST)
# File này giúp test local trước khi DNS thật được cấu hình

Write-Host "=== LOCAL TESTING SETUP ===" -ForegroundColor Green
Write-Host ""

$hostsPath = "C:\Windows\System32\drivers\etc\hosts"
$hostEntry = "52.230.60.250    call.shareapiai.com"

Write-Host "Thêm entry vào hosts file để test local:" -ForegroundColor Yellow
Write-Host "File: $hostsPath" -ForegroundColor Cyan
Write-Host "Entry: $hostEntry" -ForegroundColor Cyan
Write-Host ""

Write-Host "CÁCH THÊM THỦ CÔNG:" -ForegroundColor Yellow
Write-Host "1. Mở Notepad as Administrator" -ForegroundColor White
Write-Host "2. Mở file: $hostsPath" -ForegroundColor White
Write-Host "3. Thêm dòng: $hostEntry" -ForegroundColor White
Write-Host "4. Lưu file" -ForegroundColor White
Write-Host ""

Write-Host "SAU KHI THÊM, TEST BẰNG:" -ForegroundColor Yellow
Write-Host "ping call.shareapiai.com" -ForegroundColor Cyan
Write-Host "curl http://call.shareapiai.com" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  LƯU Ý:" -ForegroundColor Red
Write-Host "- Chỉ dùng để test local" -ForegroundColor Yellow
Write-Host "- Phải xóa entry này sau khi DNS thật hoạt động" -ForegroundColor Yellow
Write-Host "- Không ai khác có thể truy cập call.shareapiai.com ngoài máy này" -ForegroundColor Yellow

# Try to add automatically (requires admin rights)
Write-Host ""
Write-Host "Thử thêm tự động..." -ForegroundColor Yellow
try {
    $currentContent = Get-Content $hostsPath -ErrorAction Stop
    if ($currentContent -notcontains $hostEntry) {
        Add-Content $hostsPath $hostEntry -ErrorAction Stop
        Write-Host "✅ Đã thêm entry vào hosts file" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Entry đã tồn tại trong hosts file" -ForegroundColor Blue
    }
} catch {
    Write-Host "❌ Cần chạy PowerShell as Administrator để tự động thêm" -ForegroundColor Red
    Write-Host "Hoặc thêm thủ công theo hướng dẫn trên" -ForegroundColor Yellow
}

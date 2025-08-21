# Cấu hình DNS cho call.shareapiai.com trên Hostinger

## Thông tin cần thiết:
- **Static IP Azure:** 52.230.60.250
- **Domain:** call.shareapiai.com
- **Verification ID:** 664F5BF931382C5EF3D5F87B9514F5039B9E248A125642745034E5F34BC8CB01
- **Nameservers:** ns1.dns-parking.com, ns2.dns-parking.com

## Bước 1: Đăng nhập Hostinger Control Panel

1. Truy cập: https://hpanel.hostinger.com
2. Đăng nhập với tài khoản Hostinger của bạn
3. Chọn domain **shareapiai.com**

## Bước 2: Cấu hình DNS Zone

### Vào DNS Zone Editor:
1. Trong hPanel, chọn **Domains**
2. Chọn **shareapiai.com**
3. Chọn **DNS Zone Editor** (hoặc **Manage DNS**)

### Thêm 2 DNS Records sau:

#### Record 1: A Record (cho subdomain call)
```
Type: A
Name: call
Target/Value: 52.230.60.250
TTL: 14400 (hoặc để mặc định)
```

#### Record 2: TXT Record (cho Azure verification)
```
Type: TXT
Name: asuid.call
Content/Value: 664F5BF931382C5EF3D5F87B9514F5039B9E248A125642745034E5F34BC8CB01
TTL: 14400 (hoặc để mặc định)
```

## Bước 3: Lưu và chờ propagation

1. **Save/Apply** changes
2. Chờ DNS propagation (5-60 phút)
3. Có thể kiểm tra bằng online DNS checker

## Bước 4: Verification Commands

Sau khi DNS đã propagate, chạy các lệnh sau để kiểm tra:

```powershell
# Kiểm tra A record
nslookup call.shareapiai.com

# Kiểm tra TXT record
nslookup -type=TXT asuid.call.shareapiai.com

# Hoặc dùng dig (nếu có)
dig call.shareapiai.com
dig asuid.call.shareapiai.com TXT
```

## Bước 5: Cấu hình Azure (sau khi DNS hoạt động)

```bash
# Add hostname to container app
az containerapp hostname add --name litellm-app --resource-group rg-litellm --hostname call.shareapiai.com

# Create managed certificate
az containerapp env certificate create --name litellm-env --resource-group rg-litellm --certificate-name shareapiai-cert --hostname call.shareapiai.com --validation-method HTTP

# Bind certificate
az containerapp hostname bind --name litellm-app --resource-group rg-litellm --hostname call.shareapiai.com --environment litellm-env
```

## Screenshot hướng dẫn Hostinger:

### Trong DNS Zone Editor, bạn sẽ thấy form như sau:

**Thêm A Record:**
- Type: `A`
- Name: `call`
- Points to: `52.230.60.250`
- TTL: `14400`

**Thêm TXT Record:**
- Type: `TXT`
- Name: `asuid.call`
- Content: `664F5BF931382C5EF3D5F87B9514F5039B9E248A125642745034E5F34BC8CB01`
- TTL: `14400`

## Troubleshooting:

1. **Nếu không thấy DNS Zone Editor:**
   - Kiểm tra nameservers có đúng là Hostinger không
   - Đảm bảo domain đã active

2. **Nếu DNS không propagate:**
   - Chờ thêm thời gian (có thể 2-6 giờ)
   - Xóa DNS cache: `ipconfig /flushdns`
   - Kiểm tra bằng tool online: whatsmydns.net

3. **Nếu Azure validation fail:**
   - Đảm bảo TXT record chính xác 100%
   - Kiểm tra không có space thừa
   - Thử lại sau 30 phút

## Kết quả mong đợi:

Sau khi hoàn thành, bạn có thể truy cập:
- **HTTP:** http://call.shareapiai.com (redirect to HTTPS)
- **HTTPS:** https://call.shareapiai.com
- **API:** https://call.shareapiai.com/health/liveliness

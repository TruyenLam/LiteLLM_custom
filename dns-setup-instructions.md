# DNS Configuration cho call.shareapiai.com

## Bước 1: Cấu hình DNS Records

Bạn cần tạo các DNS records sau trong domain provider của shareapiai.com:

### 1. A Record (cho traffic routing)
```
Type: A
Name: call
Value: 52.230.60.250
TTL: 300 (hoặc default)
```

### 2. TXT Record (cho domain verification)
```
Type: TXT
Name: asuid.call
Value: 664F5BF931382C5EF3D5F87B9514F5039B9E248A125642745034E5F34BC8CB01
TTL: 300 (hoặc default)
```

## Bước 2: Sau khi cấu hình DNS

Sau khi bạn đã thêm cả 2 DNS records trên vào domain provider, chạy các lệnh sau:

```bash
# Verify DNS records
nslookup call.shareapiai.com
nslookup asuid.call.shareapiai.com -type=TXT

# Add hostname to container app
az containerapp hostname add --name litellm-app --resource-group rg-litellm --hostname call.shareapiai.com

# Create managed certificate
az containerapp env certificate create --name litellm-env --resource-group rg-litellm --certificate-name shareapiai-cert --hostname call.shareapiai.com --validation-method HTTP

# Bind certificate to hostname
az containerapp hostname bind --name litellm-app --resource-group rg-litellm --hostname call.shareapiai.com --environment litellm-env
```

## Thông tin quan trọng:

- **Static IP:** 52.230.60.250
- **Custom Domain:** call.shareapiai.com
- **Verification ID:** 664F5BF931382C5EF3D5F87B9514F5039B9E248A125642745034E5F34BC8CB01

## Verification Commands:

```bash
# Check if DNS has propagated
dig call.shareapiai.com
dig asuid.call.shareapiai.com TXT

# Check container app status
az containerapp show --name litellm-app --resource-group rg-litellm --query "properties.configuration.ingress"
```

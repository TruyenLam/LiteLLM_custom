# Azure Container Apps - LiteLLM Cost Optimized Configuration

## Resource Summary

### LiteLLM App (External Access)
- **URL:** https://litellm-app.prouddesert-5ea23a02.southeastasia.azurecontainerapps.io
- **Access:** External (Internet accessible)
- **Scaling:** 0-3 replicas (Scale to Zero enabled)
- **Resources:** 0.25 CPU, 0.5GB Memory
- **Auto-scaling:** HTTP rule with 30 concurrent requests threshold
- **Environment Variables:**
  - DATABASE_URL: PostgreSQL connection
  - STORE_MODEL_IN_DB: True
  - LITELLM_MASTER_KEY: sk-hWv1u2fX3yG4zJ5kT6p7qR8sT9uV0wX1
  - LITELLM_SALT_KEY: sk-aB2c3D4eF5g6H7i8J9k0L1m2N3o4P5qR

### Prometheus App (Internal Only)
- **URL:** prometheus-app.internal.prouddesert-5ea23a02.southeastasia.azurecontainerapps.io
- **Access:** Internal only (No internet access)
- **Scaling:** 0-2 replicas (Scale to Zero enabled)
- **Resources:** 0.25 CPU, 0.5GB Memory
- **Auto-scaling:** Basic scaling (no specific rules)

## Cost Optimization Features

### Scale to Zero
- ✅ Both apps configured with `minReplicas: 0`
- ✅ Apps automatically shutdown when no traffic
- ✅ Cold start when traffic arrives (typically 2-5 seconds)

### Minimal Resources
- ✅ Reduced CPU: 0.25 vCPU (from default 0.5)
- ✅ Reduced Memory: 0.5GB (from default 1GB)
- ✅ Consumption pricing tier

### Network Optimization
- ✅ Prometheus internal-only (no egress charges for external access)
- ✅ Internal communication between apps (no external traffic costs)

## Estimated Monthly Costs (Southeast Asia)

### When Running (per hour):
- **LiteLLM:** ~$0.0125/hour per replica
- **Prometheus:** ~$0.0125/hour per replica
- **Total when both running:** ~$0.025/hour

### Scale to Zero Benefits:
- **No traffic periods:** $0.00/hour
- **Environment overhead:** ~$0.000036/hour
- **Estimated monthly (with scale to zero):** $5-20 USD/month

## Commands to Monitor

```bash
# Check app status
az containerapp list --resource-group rg-litellm --output table

# Check replica count
az containerapp replica list --name litellm-app --resource-group rg-litellm

# Check logs
az containerapp logs show --name litellm-app --resource-group rg-litellm --tail 20

# Manual scale (if needed)
az containerapp scale --name litellm-app --resource-group rg-litellm --replicas 1
```

## Internal Communication

- LiteLLM → Prometheus: `prometheus-app:9090`
- Prometheus → LiteLLM: `litellm-app:4000/metrics`

## Security
- ✅ Prometheus not accessible from internet
- ✅ Environment variables stored securely
- ✅ Internal network communication
- ✅ HTTPS termination at ingress

# LiteLLM Custom - AI Model Gateway

🚀 **LiteLLM proxy server với AIMLAPI integration** - Một gateway thống nhất cho nhiều AI models qua một API endpoint duy nhất.

## ✨ Features

- 🔄 **Multi-Provider Support**: OpenAI, Anthropic, Google, Meta models via AIMLAPI
- 🌐 **Unified API**: OpenAI-compatible endpoints cho tất cả models
- 📊 **Database Persistence**: PostgreSQL cho model management và logging
- 🔐 **Secure**: API key authentication và environment variable protection
- 📈 **Monitoring**: Health checks và metrics với Prometheus
- 🚀 **Railway Ready**: Optimized cho Railway.app deployment

## 🎯 Supported Models

### Via AIMLAPI Integration:
- **ChatGPT-4o Latest** - Most capable OpenAI model
- **ChatGPT-4o** - Advanced reasoning và vision
- **ChatGPT-4o Mini** - Cost-effective option
- **GPT-4 Turbo** - High performance
- **Claude 3.5 Sonnet** - Excellent reasoning (Anthropic)
- **Gemini 1.5 Pro** - Google's flagship model
- **Llama 3.1 70B/8B** - Meta's advanced models

## 🚀 Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

### 1. Fork this repo
```bash
git clone https://github.com/yourusername/LiteLLM_custom.git
cd LiteLLM_custom
```

### 2. Deploy to Railway
1. Connect GitHub repo to Railway
2. Set environment variables:
   ```
   AIMLAPI_KEY=your_aimlapi_key
   LITELLM_MASTER_KEY=your_chosen_master_key
   LITELLM_SALT_KEY=your_salt_key
   DATABASE_URL=postgresql://user:pass@host:port/db
   STORE_MODEL_IN_DB=True
   ```
3. Railway sẽ tự động deploy từ `Dockerfile.railway`

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AIMLAPI_KEY` | API key từ AIMLAPI | ✅ |
| `LITELLM_MASTER_KEY` | Master key cho authentication | ✅ |
| `LITELLM_SALT_KEY` | Salt key cho encryption/decryption | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `STORE_MODEL_IN_DB` | Store models in database | ✅ |

## 📡 API Usage

### Chat Completions
```bash
curl -X POST https://your-railway-domain.railway.app/v1/chat/completions \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chatgpt-4o-latest",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### List Available Models
```bash
curl -H "Authorization: Bearer YOUR_MASTER_KEY" \
     https://your-railway-domain.railway.app/v1/models
```

### Health Check
```bash
curl https://your-railway-domain.railway.app/health/liveliness
```

## 🏗️ Local Development

### Prerequisites
- Docker & Docker Compose
- Python 3.8+ (optional, for scripts)

### Run Local Server
```bash
# Clone repo
git clone https://github.com/yourusername/LiteLLM_custom.git
cd LiteLLM_custom

# Copy environment file
cp .env.example .env
# Edit .env with your keys

# Start with Docker Compose
docker compose up -d

# Server available at http://localhost:4000
```

### Test Local Server
```bash
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chatgpt-4o-latest", 
    "messages": [{"role": "user", "content": "Test message"}]
  }'
```

## 📊 Monitoring

- **Health Check**: `/health/liveliness`
- **Metrics**: `/metrics` (Prometheus format)
- **Model Info**: `/model/info`
- **Database**: Models được lưu trong PostgreSQL cho persistence

## 🔧 Configuration

Xem `railway_config.yaml` để customize:
- Model parameters
- Timeout settings  
- Retry logic
- Database settings

## 🔐 Security

- ✅ HTTPS/TLS encryption
- ✅ API key authentication required
- ✅ Environment variables cho sensitive data
- ✅ Request logging cho auditing

## 💰 Cost Optimization

- 🌍 **Multi-provider**: Chọn model tốt nhất cho từng task
- 📊 **Usage tracking**: Monitor costs qua database logs
- ⚡ **Efficient routing**: Load balancing và failover
- 🎯 **Model variety**: Từ cost-effective đến high-performance

## 🛠️ Tech Stack

- **LiteLLM**: Proxy server và model gateway
- **AIMLAPI**: AI model provider với 200+ models
- **PostgreSQL**: Database persistence
- **Railway**: Cloud deployment platform
- **Docker**: Containerization
- **Prometheus**: Metrics và monitoring

## 📈 Performance

- ⚡ **Low latency**: Direct API calls với minimal overhead
- 🔄 **Auto-retry**: Built-in retry logic cho reliability
- 📊 **Load balancing**: Distribute requests across models
- 🚀 **Scalable**: Railway auto-scaling

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📝 License

MIT License - xem [LICENSE](LICENSE) file

## 🆘 Support

- 📖 [LiteLLM Docs](https://docs.litellm.ai/)
- 🚂 [Railway Docs](https://docs.railway.app/)
- 🤖 [AIMLAPI Docs](https://aimlapi.com/docs)
- 💬 [Issues](https://github.com/yourusername/LiteLLM_custom/issues)

---

**Made with ❤️ for the AI community**

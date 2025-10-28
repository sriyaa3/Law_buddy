# Deployment Guide - AskLegal Enhanced

## System Requirements

### Minimum Requirements
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Storage**: 20 GB available space
- **OS**: Linux, macOS, or Windows 10+
- **Python**: 3.8+

### Recommended Requirements
- **CPU**: 8 cores
- **RAM**: 16 GB
- **Storage**: 50 GB available space
- **GPU**: CUDA-compatible GPU (optional, for faster inference)

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd asklegal_enhanced
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Language Models
```bash
python download_model.py
```

### 5. Install spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

## Service Dependencies

### Redis (Optional but Recommended)
Redis is used for metadata storage and fast lookups.

```bash
# Using Docker
docker run -d -p 6379:6379 --name asklegal-redis redis:alpine

# Or install directly
# On Ubuntu/Debian:
sudo apt-get install redis-server

# On macOS:
brew install redis
```

### Neo4j (Optional but Recommended)
Neo4j is used for the legal knowledge graph.

```bash
# Using Docker
docker run -d -p 7474:7474 -p 7687:7687 --name asklegal-neo4j neo4j:latest

# Access Neo4j Browser at http://localhost:7474
# Default credentials: neo4j/neo4j (change password on first login)
```

## Environment Configuration

Create a `.env` file in the project root:

```env
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

# SLM Configuration
MODEL_PATH=./models

# Server Configuration
HOST=0.0.0.0
PORT=8006
```

## Starting the Application

### Development Mode
```bash
# Make startup script executable
chmod +x start.sh

# Start the application
./start.sh
```

### Production Mode
For production deployment, use a process manager like `supervisor` or `pm2`:

```bash
# Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8006 --workers 4

# Using gunicorn (if installed)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8006
```

## Docker Deployment (Recommended for Production)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8006:8006"
    environment:
      - REDIS_HOST=redis
      - NEO4J_URI=bolt://neo4j:7687
    depends_on:
      - redis
      - neo4j
    volumes:
      - ./models:/app/models
      - ./data:/app/data
      - ./uploads:/app/uploads

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  neo4j:
    image: neo4j:latest
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/password
    volumes:
      - neo4j_data:/data

volumes:
  neo4j_data:
```

Start with Docker Compose:
```bash
docker-compose up -d
```

## Reverse Proxy Configuration

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8006;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Apache Configuration
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    ProxyPreserveHost On
    ProxyPass / http://localhost:8006/
    ProxyPassReverse / http://localhost:8006/
</VirtualHost>
```

## SSL/HTTPS Configuration

Using Let's Encrypt with Certbot:

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com
```

## Monitoring and Logging

### Application Logs
Logs are written to the console by default. For file logging, configure in `app/main.py`:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks
The application provides a health check endpoint:
```
GET /health
```

## Backup and Recovery

### Data Backup
```bash
# Backup FAISS indices
tar -czf faiss_backup_$(date +%Y%m%d).tar.gz data/

# Backup Redis (if using persistence)
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb redis_backup_$(date +%Y%m%d).rdb

# Backup Neo4j
neo4j-admin dump --database=neo4j --to=neo4j_backup_$(date +%Y%m%d).dump
```

### Model Backup
```bash
# Backup SLM models
tar -czf models_backup_$(date +%Y%m%d).tar.gz models/
```

## Performance Tuning

### FAISS Configuration
Adjust FAISS index parameters in `app/vector_store/faiss_store.py` for your use case.

### SLM Parameters
Tune generation parameters in `app/slm/engines/ctransformers_engine.py`:
```python
self.config = {
    "max_new_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "repetition_penalty": 1.1
}
```

### Uvicorn Workers
For production, use multiple workers:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8006 --workers 4
```

## Security Considerations

### Firewall Configuration
```bash
# Allow only necessary ports
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw allow 8006  # Application (internal only in production)
ufw enable
```

### API Security
- Use API keys for sensitive endpoints
- Implement rate limiting
- Validate all inputs
- Use HTTPS in production

### Data Privacy
- Implement data retention policies
- Encrypt sensitive data at rest
- Use privacy-preserving techniques for PII
- Comply with local data protection regulations

## Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure models are downloaded: `python download_model.py`
   - Check model path in `.env` file

2. **Database Connection Issues**
   - Verify Redis and Neo4j are running
   - Check connection credentials in `.env` file

3. **Memory Issues**
   - Reduce `max_new_tokens` in SLM configuration
   - Use quantized models
   - Add swap space if necessary

4. **Performance Issues**
   - Monitor system resources
   - Optimize FAISS indices
   - Scale horizontally with multiple workers

### Logs and Debugging
Check application logs for error messages:
```bash
# View recent logs
tail -f app.log

# Search for specific errors
grep "ERROR" app.log
```

## Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart the application
./start.sh
```

### Model Updates
```bash
# Check for new models
python download_model.py --list

# Download specific model
python download_model.py --model model_name
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer for multiple app instances
- Shared Redis and Neo4j instances
- Distributed file storage for uploads

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Use GPU acceleration for inference

This deployment guide provides a comprehensive approach to running AskLegal Enhanced in production environments while maintaining security, performance, and reliability.
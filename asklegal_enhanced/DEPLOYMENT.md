# AskLegal Enhanced - Deployment Guide

## Quick Start

### Option 1: Automatic Setup (Recommended)

```bash
cd asklegal_enhanced
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Step-by-Step Setup

```bash
cd asklegal_enhanced

# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Setup models
python setup_models.py

# Step 3: Initialize services
python initialize_services.py

# Step 4: Start application
python start_enhanced.py
```

### Option 3: Using Supervisor (Production)

```bash
cd asklegal_enhanced

# Install supervisor
sudo apt-get install supervisor

# Copy config
sudo cp supervisord.conf /etc/supervisor/conf.d/asklegal.conf

# Start services
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start asklegal_backend
```

## System Requirements

### Minimum Requirements
- Python 3.8+
- 4GB RAM
- 5GB disk space
- Ubuntu 18.04+ or similar Linux distribution

### Recommended Requirements
- Python 3.10+
- 8GB RAM
- 10GB disk space
- SSD storage

## Dependencies

### Python Packages (Installed Automatically)
- FastAPI - Web framework
- Uvicorn - ASGI server
- PyTorch - Deep learning framework
- Transformers - Model handling
- Sentence-Transformers - Embeddings
- FAISS - Vector similarity search
- SQLAlchemy - Database ORM
- Pydantic - Data validation

### Optional Services
- **Redis** (optional): For caching and metadata storage
  - Install: `sudo apt-get install redis-server`
  - The application will use in-memory fallback if not available

- **Neo4j** (optional): For graph-based legal knowledge representation
  - Install: Follow [Neo4j installation guide](https://neo4j.com/docs/operations-manual/current/installation/)
  - The application will use fallback if not available

## Environment Configuration

Create a `.env` file in the `asklegal_enhanced` directory:

```bash
# Application Settings
PROJECT_NAME="AskLegal Enhanced"
SECRET_KEY="your-secret-key-here"

# Database
DATABASE_URL="sqlite:///./asklegal.db"

# Redis (optional)
REDIS_HOST="localhost"
REDIS_PORT=6379

# Neo4j (optional)
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="password"

# Paths
MODEL_PATH="./models"
UPLOAD_DIR="./uploads"
DATA_DIR="./data"
```

## Port Configuration

Default ports:
- **Backend API**: 8001
- **Frontend**: 3000 (development)
- **Redis**: 6379 (if using)
- **Neo4j**: 7687 (if using)

To change the backend port:
```bash
python start_enhanced.py --port 8080
```

## Testing

### Run Test Suite

```bash
# Make sure server is running first
python start_enhanced.py &

# In another terminal, run tests
python test_suite.py
```

### Manual API Testing

```bash
# Health check
curl http://localhost:8001/api/v1/docs

# Test chat endpoint
curl -X POST http://localhost:8001/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "What is IPC Section 420?", "session_id": "test-123"}'
```

## Production Deployment

### Build Frontend for Production

```bash
cd frontend
npm install
npm run build
cd ..
```

The built frontend will be served automatically by FastAPI.

### Using Supervisor

Supervisor ensures your application stays running:

```bash
# Check status
sudo supervisorctl status asklegal_backend

# Restart
sudo supervisorctl restart asklegal_backend

# View logs
sudo supervisorctl tail asklegal_backend
```

### Using Docker (Optional)

A Dockerfile is provided for containerized deployment:

```bash
# Build image
docker build -t asklegal-enhanced .

# Run container
docker run -d -p 8001:8001 --name asklegal asklegal-enhanced
```

## Troubleshooting

### Server won't start

1. Check if port is already in use:
   ```bash
   lsof -i :8001
   ```

2. Check logs:
   ```bash
   tail -f /var/log/supervisor/backend.err.log
   ```

3. Verify dependencies:
   ```bash
   pip list | grep fastapi
   ```

### Models not loading

1. Re-run model setup:
   ```bash
   python setup_models.py
   ```

2. Check disk space:
   ```bash
   df -h
   ```

3. Verify model files:
   ```bash
   ls -lh models/
   ```

### Database errors

1. Re-initialize database:
   ```bash
   rm asklegal.db
   python initialize_services.py
   ```

2. Check permissions:
   ```bash
   chmod 644 asklegal.db
   ```

### Out of memory

1. Reduce batch size in model inference
2. Use swap space:
   ```bash
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

## Performance Optimization

### For CPU-only systems
- The application uses CPU by default
- TinyLlama model is optimized for CPU inference
- Response time: 2-5 seconds per query

### For GPU systems
- Install CUDA-enabled PyTorch:
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/cu118
  ```
- Update model loading code to use GPU

### Scaling
- Use multiple Uvicorn workers:
  ```bash
  uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8001
  ```
- Deploy behind Nginx for load balancing
- Use Redis for session management

## Security Considerations

### For Production

1. Change SECRET_KEY in .env
2. Use HTTPS (configure Nginx with SSL)
3. Enable authentication
4. Set up firewall rules
5. Regular backups of database
6. Keep dependencies updated

### Environment Variables

Never commit .env file to version control:
```bash
echo ".env" >> .gitignore
```

## Monitoring

### Application Logs

```bash
# Supervisor logs
sudo tail -f /var/log/supervisor/backend.out.log
sudo tail -f /var/log/supervisor/backend.err.log

# Application logs
tail -f logs/app.log
```

### Health Monitoring

Setup a cron job to check application health:

```bash
# Add to crontab
*/5 * * * * curl -f http://localhost:8001/api/v1/docs || systemctl restart asklegal_backend
```

## Backup and Recovery

### Backup Database

```bash
# SQLite backup
cp asklegal.db asklegal.db.backup.$(date +%Y%m%d)

# Or use sqlite3
sqlite3 asklegal.db ".backup asklegal.db.backup"
```

### Backup Models and Data

```bash
tar -czf models_backup.tar.gz models/
tar -czf data_backup.tar.gz data/
```

## Support

For issues and questions:
- Check the troubleshooting section
- Review application logs
- Run the test suite: `python test_suite.py`

## License

This project is licensed under the MIT License.

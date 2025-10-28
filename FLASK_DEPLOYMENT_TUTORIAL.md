# Deploying Flask Apps to AWS EC2 with SQL Databases

This tutorial shows how to deploy a Flask application to AWS EC2 with database support, using systemd for process management and Caddy as a reverse proxy.

## Setup EC2 Instance

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install Python 3.11 and pip
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install additional system dependencies
sudo apt install -y build-essential curl git rsync

# Verify Python installation
python3.11 --version
pip3 --version
```

## Transfer Your Application

```bash
# Transfer your Flask app to EC2 (exclude unnecessary files)
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude '.env' --exclude '__pycache__' --exclude '*.pyc' \
-e "ssh -i ~/.ssh/your-key.pem" \
/Users/mikekwak/Desktop/UNIfy-Prod/backend/ ubuntu@your-ec2-ip:~/app
```

## Database Setup

### Option 1: MySQL

```bash
# Install MySQL
sudo apt install -y mysql-server

# Start and enable MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root

# In MySQL prompt:
CREATE DATABASE unify_app;
CREATE USER 'unify_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourSecurePassword123!';
GRANT ALL PRIVILEGES ON unify_app.* TO 'unify_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Option 2: PostgreSQL

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE unify_app;
CREATE USER unify_user WITH PASSWORD 'YourSecurePassword123!';
GRANT ALL PRIVILEGES ON DATABASE unify_app TO unify_user;
\q
```

## Python Environment Setup

```bash
# Navigate to your app directory
cd ~/app

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install additional production dependencies
pip install gunicorn psycopg2-binary PyMySQL

# Test your application
python app.py
```

## Environment Configuration

### Step 1: Create the Environment File

```bash
# Create environment file
sudo vim /etc/unify.env
```

Add your environment variables:

```bash
# Database Configuration
DB_TYPE=mysql  # or postgresql
DB_HOST=localhost
DB_PORT=3306  # 5432 for PostgreSQL
DB_NAME=unify_app
DB_USER=unify_user
DB_PASSWORD=YourSecurePassword123!

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=8000
SECRET_KEY=your-super-secret-key-here

# CORS Configuration
FRONTEND_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Gemini AI (if using)
GEMINI_API_KEY=your-gemini-api-key

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
```

### Step 2: Secure the Environment File

```bash
# Restrict file permissions
sudo chmod 600 /etc/unify.env
sudo chown ubuntu:ubuntu /etc/unify.env
```

## Systemd Service Configuration

### Step 1: Create the systemd Service File

```bash
sudo vim /etc/systemd/system/unify.service
```

Add the following content:

```ini
[Unit]
Description=UNIfy Flask Application
After=network.target multi-user.target mysql.service

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/app
Environment=PATH=/home/ubuntu/app/venv/bin
ExecStart=/home/ubuntu/app/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 --access-logfile - --error-logfile - app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10
EnvironmentFile=/etc/unify.env
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=unify

[Install]
WantedBy=multi-user.target
```

### Step 2: Enable and Start the Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable the service
sudo systemctl enable unify.service

# Start the service
sudo systemctl start unify.service

# Check service status
sudo systemctl status unify.service
```

### Step 3: Verify Service is Running

```bash
# Check if the service is running
sudo systemctl is-active unify.service

# Check service logs
sudo journalctl -u unify.service

# Follow logs in real-time
sudo journalctl -fu unify.service

# Test the application
curl http://localhost:8000/
```

## Database Integration (Optional)

If you want to add database functionality to your Flask app, here's an example:

### Install Database Dependencies

```bash
# For MySQL
pip install PyMySQL

# For PostgreSQL
pip install psycopg2-binary

# For both
pip install SQLAlchemy Flask-SQLAlchemy
```

### Example Database Configuration

Add this to your `app.py`:

```python
from flask_sqlalchemy import SQLAlchemy
import os

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## Caddy Reverse Proxy Setup

### Step 1: Install Caddy

```bash
# Install Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

### Step 2: Configure Caddy

```bash
# Edit Caddyfile
sudo vim /etc/caddy/Caddyfile
```

For HTTP only (development):
```caddy
:80 {
    reverse_proxy localhost:8000
}
```

For HTTPS with domain (production):
```caddy
yourdomain.com {
    reverse_proxy localhost:8000
    
    # Optional: Add security headers
    header {
        # Enable HSTS
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        
        # Prevent clickjacking
        X-Frame-Options "SAMEORIGIN"
        
        # Prevent MIME type sniffing
        X-Content-Type-Options "nosniff"
        
        # XSS Protection
        X-XSS-Protection "1; mode=block"
    }
    
    # Optional: Logging
    log {
        output file /var/log/caddy/access.log
    }
}
```

### Step 3: Start Caddy

```bash
# Restart Caddy
sudo systemctl restart caddy

# Enable Caddy to start on boot
sudo systemctl enable caddy

# Check Caddy status
sudo systemctl status caddy
```

## SSL Certificate Setup (Optional)

Caddy automatically handles SSL certificates with Let's Encrypt. If you want to use a custom certificate:

```caddy
yourdomain.com {
    tls /path/to/cert.pem /path/to/key.pem
    reverse_proxy localhost:8000
}
```

## Monitoring and Maintenance

### View Application Logs

```bash
# View Flask app logs
sudo journalctl -u unify.service -f

# View Caddy logs
sudo journalctl -u caddy -f

# View system logs
sudo journalctl -f
```

### Restart Services

```bash
# Restart Flask app
sudo systemctl restart unify.service

# Restart Caddy
sudo systemctl restart caddy

# Restart database (if needed)
sudo systemctl restart mysql  # or postgresql
```

### Update Application

```bash
# Stop the service
sudo systemctl stop unify.service

# Pull new code (if using git)
cd ~/app
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Start the service
sudo systemctl start unify.service
```

## Security Considerations

### Firewall Setup

```bash
# Install UFW
sudo apt install ufw

# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# Enable firewall
sudo ufw enable
```

### File Permissions

```bash
# Secure your app directory
sudo chown -R ubuntu:ubuntu /home/ubuntu/app
sudo chmod -R 755 /home/ubuntu/app
sudo chmod 600 /home/ubuntu/app/.env  # if you have one
```

## Troubleshooting

### Common Issues

1. **Service won't start:**
   ```bash
   sudo journalctl -u unify.service --no-pager
   ```

2. **Database connection issues:**
   - Check database service status
   - Verify credentials in `/etc/unify.env`
   - Test connection manually

3. **Port conflicts:**
   ```bash
   sudo netstat -tlnp | grep :8000
   ```

4. **Permission issues:**
   ```bash
   sudo chown -R ubuntu:ubuntu /home/ubuntu/app
   ```

### Health Checks

```bash
# Check if Flask app is responding
curl http://localhost:8000/

# Check if Caddy is working
curl http://yourdomain.com/

# Check service status
sudo systemctl status unify.service caddy.service
```

## Production Optimizations

### Gunicorn Configuration

Create a `gunicorn.conf.py` file:

```python
# Gunicorn configuration file
bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

### Update systemd service to use config file:

```ini
ExecStart=/home/ubuntu/app/venv/bin/gunicorn --config gunicorn.conf.py app:app
```

### Database Connection Pooling

For high-traffic applications, consider using connection pooling:

```python
from sqlalchemy.pool import QueuePool

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

This completes the Flask deployment tutorial for AWS EC2. Your Flask application should now be running securely with database support, process management, and reverse proxy configuration.

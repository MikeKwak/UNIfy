# Simple Flask Deployment to AWS EC2 (No Database)

This is a simplified tutorial for deploying a Flask application to AWS EC2 without database setup.

## Setup EC2 Instance

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install Python 3.10 (available by default)
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# Install additional system dependencies
sudo apt install -y build-essential curl git rsync

# Verify Python installation
python3.10 --version
pip3 --version
```

## Transfer Your Application

```bash
# Transfer your Flask app to EC2 (exclude unnecessary files)
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude '.env' --exclude '__pycache__' --exclude '*.pyc' \
-e "ssh -i ~/.ssh/your-key.pem" \
/Users/mikekwak/Desktop/UNIfy-Prod/backend/ ubuntu@your-ec2-ip:~/app
```

## Python Environment Setup

```bash
# Navigate to your app directory
cd ~/app

# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

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
After=network.target multi-user.target

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
```

## Troubleshooting

### Common Issues

1. **Service won't start:**
   ```bash
   sudo journalctl -u unify.service --no-pager
   ```

2. **Port conflicts:**
   ```bash
   sudo netstat -tlnp | grep :8000
   ```

3. **Permission issues:**
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

## Quick Start Commands

Here's a quick reference for the essential commands:

```bash
# 1. Setup Python
sudo apt update && sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# 2. Setup app
cd ~/app
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Create environment file
sudo vim /etc/unify.env
# Add your environment variables

# 4. Create systemd service
sudo vim /etc/systemd/system/unify.service
# Add the service configuration

# 5. Start service
sudo systemctl daemon-reload
sudo systemctl enable unify.service
sudo systemctl start unify.service

# 6. Install and configure Caddy
sudo apt install caddy
sudo vim /etc/caddy/Caddyfile
# Add your domain configuration
sudo systemctl restart caddy
```

That's it! Your Flask app should now be running and accessible via your domain.

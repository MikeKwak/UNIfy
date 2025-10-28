# Local Flask Development Setup on macOS

## Prerequisites

### Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install Python and Dependencies
```bash
# Install Python 3.11
brew install python@3.11

# Install MySQL (if you want local database)
brew install mysql

# Install PostgreSQL (alternative database)
brew install postgresql

# Install other tools
brew install git curl
```

## Setup Your Flask Application

### 1. Navigate to your backend directory
```bash
cd /Users/mikekwak/Desktop/UNIfy-Prod/backend
```

### 2. Create virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create local environment file
```bash
cp env.development .env
```

### 5. Start MySQL (if using)
```bash
brew services start mysql
```

### 6. Create database
```bash
mysql -u root -p
# In MySQL prompt:
CREATE DATABASE unify_app;
CREATE USER 'unify_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON unify_app.* TO 'unify_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 7. Run your Flask application
```bash
python app.py
```

## For Production Deployment

If you want to deploy to AWS EC2, you would:

1. **Launch an EC2 instance:**
   - Go to AWS Console → EC2
   - Launch instance with Ubuntu 22.04 LTS
   - Configure security groups (ports 22, 80, 443)
   - Download your key pair (.pem file)

2. **Connect to your EC2 instance:**
   ```bash
   ssh -i ~/.ssh/your-key.pem ubuntu@your-ec2-ip
   ```

3. **Then follow the original tutorial** on the EC2 instance

## Alternative: Use Docker for Local Development

You can also run your Flask app in Docker locally:

```bash
# Build the Docker image
docker build -t unify-backend .

# Run the container
docker run -p 8000:8000 --env-file env.development unify-backend
```

## Quick Test

To test if everything is working locally:

```bash
# In your backend directory
cd /Users/mikekwak/Desktop/UNIfy-Prod/backend
source venv/bin/activate
python app.py
```

Then visit `http://localhost:8000` in your browser.

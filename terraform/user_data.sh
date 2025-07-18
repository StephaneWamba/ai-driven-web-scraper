#!/bin/bash

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3 python3-pip python3-venv nginx git curl

# Create application directory
sudo mkdir -p /home/ubuntu/ai-scraper
sudo chown ubuntu:ubuntu /home/ubuntu/ai-scraper

# Clone the repository
cd /home/ubuntu
git clone https://github.com/your-username/ai-driven-web-scraper.git ai-scraper
cd ai-scraper

# Set up backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service for backend
sudo tee /etc/systemd/system/ai-scraper-backend.service > /dev/null <<EOF
[Unit]
Description=AI Scraper Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-scraper/backend
Environment=PATH=/home/ubuntu/ai-scraper/backend/venv/bin
ExecStart=/home/ubuntu/ai-scraper/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start backend service
sudo systemctl daemon-reload
sudo systemctl enable ai-scraper-backend
sudo systemctl start ai-scraper-backend

# Set up frontend
cd ../frontend
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
npm install
npm run build

# Configure nginx
sudo tee /etc/nginx/sites-available/ai-scraper > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    # Frontend
    location / {
        root /home/ubuntu/ai-scraper/frontend/build;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Health check
    location /health {
        proxy_pass http://localhost:8000/health;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/ai-scraper /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

# Set up automatic updates
sudo tee /etc/cron.daily/update-ai-scraper > /dev/null <<EOF
#!/bin/bash
cd /home/ubuntu/ai-scraper
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart ai-scraper-backend
cd ../frontend
npm install
npm run build
sudo systemctl restart nginx
EOF

sudo chmod +x /etc/cron.daily/update-ai-scraper

echo "Setup complete! Backend running on port 8000, frontend served by nginx on port 80" 
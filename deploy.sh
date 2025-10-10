#!/bin/bash

# Deploy ADS reader to server
SERVER="mustry@mustry-server.broeve"
REMOTE_DIR="~/ads-tester"

echo "Deploying ADS reader to $SERVER..."

# Create remote directory
ssh $SERVER "mkdir -p $REMOTE_DIR"

# Copy all project files
echo "Copying files..."
scp ads_reader.py $SERVER:$REMOTE_DIR/
scp config.json $SERVER:$REMOTE_DIR/
scp ads_config.yaml $SERVER:$REMOTE_DIR/
scp requirements.txt $SERVER:$REMOTE_DIR/
scp config_example.py $SERVER:$REMOTE_DIR/

echo "Files copied successfully!"

# Set up and run on server
echo "Setting up environment on server..."
ssh $SERVER << 'EOF'
cd ~/ads-tester

# Create virtual environment
python3 -m venv venv

# Activate and install dependencies
source venv/bin/activate
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the ADS reader:"
echo "  ssh mustry@mustry-server.broeve"
echo "  cd ads-tester"
echo "  source venv/bin/activate"
echo "  python ads_reader.py"
EOF

echo "Deployment complete!"
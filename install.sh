#!/bin/bash
# Installer for Stealth Mode Tray App

echo "Installing Stealth Mode Tray App..."

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
USER_NAME=$USER

# 1. Make backend executable
chmod +x "$DIR/stealth-backend.sh"

# 2. Setup Sudoers drop-in so it doesn't ask for a password every time you toggle
SUDOERS_FILE="/etc/sudoers.d/stealth-mode"
echo "Setting up sudoers rule (requires sudo password)..."
sudo bash -c "cat > $SUDOERS_FILE" << EOF
$USER_NAME ALL=(root) NOPASSWD: $DIR/stealth-backend.sh
EOF
sudo chmod 0440 "$SUDOERS_FILE"

# 3. Setup Python virtual environment (recommended for python tray apps)
echo "Setting up Python virtual environment with system packages (for GTK/AppIndicator)..."
python3 -m venv --system-site-packages "$DIR/venv"
"$DIR/venv/bin/pip" install -r "$DIR/requirements.txt"

# 4. Create Systemd User Service for robust autostart
SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"
SERVICE_FILE="$SERVICE_DIR/stealth-mode.service"

echo "Setting up systemd user service..."
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Stealth Mode Tray App
After=graphical-session.target

[Service]
Type=simple
Environment="PYSTRAY_BACKEND=appindicator"
ExecStart=$DIR/venv/bin/python $DIR/main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now stealth-mode.service

echo "Installation complete!"
echo "The Stealth Mode service is now running and will start automatically on login."
echo "You can check its status with: systemctl --user status stealth-mode.service"

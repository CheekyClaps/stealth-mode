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
echo "Setting up Python virtual environment..."
python3 -m venv "$DIR/venv"
"$DIR/venv/bin/pip" install -r "$DIR/requirements.txt"

# 4. Create Desktop Entry for Autostart
AUTOSTART_DIR="$HOME/.config/autostart"
mkdir -p "$AUTOSTART_DIR"
DESKTOP_FILE="$AUTOSTART_DIR/stealth-mode.desktop"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Type=Application
Name=Stealth Mode
Comment=Toggle network stealth mode
Exec=$DIR/venv/bin/python $DIR/main.py
Terminal=false
StartupNotify=false
Categories=Utility;Network;
EOF

chmod +x "$DESKTOP_FILE"

echo "Installation complete!"
echo "To start it now, run: $DIR/venv/bin/python $DIR/main.py"
echo "It will also start automatically on your next login."

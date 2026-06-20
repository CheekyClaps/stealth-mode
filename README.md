# Stealth Mode Tray App

A lightweight system tray application for Linux (specifically targeted at Fedora/GNOME) that allows you to quickly toggle a "Stealth Mode" state.

When activated, Stealth Mode hardens your network presence by:
1. Stopping the `avahi-daemon` (mDNS) to prevent local network discovery.
2. Stopping background DNF package cache updates.
3. Setting the default `firewalld` zone to `drop`, blocking all incoming unsolicited traffic.

## Requirements

*   Python 3
*   `sudo` access (the installer configures a passwordless sudo rule for the backend script)
*   `systemd` (for the user background service)
*   **System Packages:** You need PyGObject and native AppIndicator libraries.
    *   On Fedora: `sudo dnf install python3-gobject libayatana-appindicator-gtk3`

## Installation

Run the provided installation script. It will set up a Python virtual environment, configure the `sudoers` rule, and register a systemd user service.

```bash
./install.sh
```

Once installed, the tray icon will automatically start when you log in. The service is managed via user-level systemd:

```bash
# Check status
systemctl --user status stealth-mode.service

# Restart the app
systemctl --user restart stealth-mode.service
```

## How it Works

*   **`main.py`**: The frontend system tray app written in Python using `PyGObject` and `AppIndicator3`. It renders a dynamic spy hat/sunglasses icon that turns bright white when Stealth Mode is active and grayed out when disabled.
*   **`stealth-backend.sh`**: The backend bash script that executes the necessary system and firewall commands. It is run via `sudo` by the frontend app.

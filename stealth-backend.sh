#!/bin/bash
# Backend script for Stealth Mode
# Needs to run as root.

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

case "$1" in
  on)
    # 1. Stop Avahi (mDNS)
    systemctl stop avahi-daemon.socket avahi-daemon.service 2>/dev/null
    
    # 2. Stop DNF background updates
    systemctl stop dnf-makecache.timer 2>/dev/null
    
    # 3. Set Firewall to Drop (block unsolicited traffic)
    firewall-cmd --set-default-zone=drop > /dev/null
    
    # Optional: block systemd-resolved LLMNR if you want dynamic config
    # but that usually requires modifying resolved.conf.
    
    echo "stealth_on"
    ;;
  off)
    # 1. Restore Avahi
    systemctl start avahi-daemon.socket avahi-daemon.service 2>/dev/null
    
    # 2. Restore DNF background updates
    systemctl start dnf-makecache.timer 2>/dev/null
    
    # 3. Restore default Fedora firewall profile
    firewall-cmd --set-default-zone=FedoraWorkstation > /dev/null
    
    echo "stealth_off"
    ;;
  status)
    ZONE=$(firewall-cmd --get-default-zone)
    if [ "$ZONE" == "drop" ]; then
      echo "stealth_on"
    else
      echo "stealth_off"
    fi
    ;;
  *)
    echo "Usage: $0 {on|off|status}"
    exit 1
    ;;
esac

import os
import subprocess
import threading
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item

BACKEND_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stealth-backend.sh")

def run_backend(command):
    """Run the backend shell script via sudo and return the output."""
    try:
        # Since we will set up a sudoers NOPASSWD rule, this won't prompt.
        result = subprocess.run(
            ["sudo", BACKEND_SCRIPT, command],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running backend: {e}")
        return None

def get_status():
    """Check if stealth mode is currently active."""
    status = run_backend("status")
    return status == "stealth_on"

def create_image(is_stealth):
    """Generate a 'Stealth/Spy' icon (Hat and Sunglasses)."""
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    if is_stealth:
        # Active: Bright white
        c = (240, 240, 240, 255)
    else:
        # Inactive: Greyed out / semi-transparent
        c = (120, 120, 120, 150)
        
    # Draw Hat Top
    draw.polygon([(20, 12), (44, 12), (46, 28), (18, 28)], fill=c)
    
    # Draw Hat Brim
    draw.ellipse((10, 24, 54, 34), fill=c)
    
    # Draw Sunglasses Left Lens
    draw.ellipse((16, 38, 30, 52), fill=c)
    
    # Draw Sunglasses Right Lens
    draw.ellipse((34, 38, 48, 52), fill=c)
    
    # Draw Sunglasses Bridge
    draw.rectangle((30, 42, 34, 46), fill=c)
        
    return image

def on_toggle(icon, item):
    """Handle the toggle action from the menu."""
    current_state = get_status()
    new_state = not current_state
    
    command = "on" if new_state else "off"
    run_backend(command)
    
    update_icon(icon)

def update_icon(icon):
    """Update the tray icon image and menu based on the current state."""
    is_stealth = get_status()
    icon.icon = create_image(is_stealth)
    icon.title = "Stealth Mode: ON" if is_stealth else "Stealth Mode: OFF"

def setup(icon):
    """Initial setup when tray is ready."""
    update_icon(icon)

def quit_app(icon, item):
    icon.stop()

def main():
    # Initial state doesn't matter much as update_icon will fix it
    icon_image = create_image(False)
    
    menu = pystray.Menu(
        item(lambda text: "Disable Stealth Mode" if get_status() else "Enable Stealth Mode", on_toggle),
        pystray.Menu.SEPARATOR,
        item('Quit', quit_app)
    )
    
    icon = pystray.Icon("stealth-mode", icon_image, "Stealth Mode", menu)
    
    # Run the tray icon application
    icon.run(setup)

if __name__ == "__main__":
    main()

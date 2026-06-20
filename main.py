import os
import subprocess
import tempfile
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
from PIL import Image, ImageDraw

BACKEND_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stealth-backend.sh")

class StealthApp:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "stealth-mode-indicator",
            "",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        self.icon_temp_dir = tempfile.mkdtemp()
        self.update_ui()
        
        # We need to run the initial status check and update periodically
        # or listen for changes. For simplicity, we just update it on toggle.

    def run_backend(self, command):
        """Run the backend shell script via sudo and return the output."""
        try:
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

    def get_status(self):
        """Check if stealth mode is currently active."""
        status = self.run_backend("status")
        return status == "stealth_on"

    def create_image(self, is_stealth):
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

    def update_ui(self):
        """Update the icon and menu based on the current state."""
        is_stealth = self.get_status()
        
        # AppIndicator requires a file path or an icon name from the theme.
        # Since we generate it dynamically, we save it to a temporary file.
        icon_path = os.path.join(self.icon_temp_dir, f"stealth_icon_{is_stealth}.png")
        if not os.path.exists(icon_path):
            img = self.create_image(is_stealth)
            img.save(icon_path)
            
        self.indicator.set_icon_full(icon_path, "Stealth Mode Icon")
        self.indicator.set_title("Stealth Mode: ON" if is_stealth else "Stealth Mode: OFF")
        
        self.build_menu(is_stealth)

    def build_menu(self, is_stealth):
        menu = Gtk.Menu()
        
        toggle_item = Gtk.MenuItem(label="Disable Stealth Mode" if is_stealth else "Enable Stealth Mode")
        toggle_item.connect("activate", self.on_toggle)
        menu.append(toggle_item)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit_app)
        menu.append(quit_item)
        
        menu.show_all()
        self.indicator.set_menu(menu)

    def on_toggle(self, widget):
        current_state = self.get_status()
        new_state = not current_state
        command = "on" if new_state else "off"
        self.run_backend(command)
        
        # Update UI in idle loop to keep UI responsive
        GLib.idle_add(self.update_ui)

    def quit_app(self, widget):
        Gtk.main_quit()

def main():
    app = StealthApp()
    Gtk.main()

if __name__ == "__main__":
    main()

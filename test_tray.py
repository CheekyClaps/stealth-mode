import time
import threading
import pystray
from PIL import Image, ImageDraw
import gi
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3

def create_image(color):
    image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((12, 12, 52, 52), fill=color)
    return image

img_red = create_image("red")
img_blue = create_image("blue")

def setup(icon):
    icon.visible = True
    def toggle():
        state = False
        while True:
            time.sleep(2)
            state = not state
            icon.icon = img_blue if state else img_red
            print("Switched to", "blue" if state else "red")
    threading.Thread(target=toggle, daemon=True).start()

menu = pystray.Menu(pystray.MenuItem('Quit', lambda icon: icon.stop()))
icon = pystray.Icon("test", img_red, "Test", menu)
icon.run(setup)

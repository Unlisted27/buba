import time, os, pathlib, json, subprocess, bubasicsconfig
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

# Singleton pattern for button objects
class _ButtonSingleton:
    _initialized = False
    def __init__(self):
        if not _ButtonSingleton._initialized:
            self.btn_up = Button(
                bubasicsconfig.buttons.btn_up_gpio,
                bounce_time=bubasicsconfig.buttons.bounce_time
            )
            self.btn_down = Button(
                bubasicsconfig.buttons.btn_down_gpio,
                bounce_time=bubasicsconfig.buttons.bounce_time
            )
            self.btn_select = Button(
                bubasicsconfig.buttons.btn_select_gpio,
                bounce_time=bubasicsconfig.buttons.bounce_time
            )
            _ButtonSingleton._initialized = True

    def cleanup(self):
        try:
            self.btn_up.close()
            self.btn_down.close()
            self.btn_select.close()
        except Exception as e:
            print(f"button cleanup error: {e}")

# Create singleton instance at import
_buttons = _ButtonSingleton()
btn_up = _buttons.btn_up
btn_down = _buttons.btn_down
btn_select = _buttons.btn_select

def button_cleanup():
    _buttons.cleanup()

def gpio_cleanup(gpiozero_button):
    """takes a gpiozero.Button object and closes it"""
    try:
        gpiozero_button.close()
    except Exception as e:
        print(f"GPIO cleanup error: {e}")

def clear_screen(device = bubasicsconfig.device):
    device.clear()

def scrnprint(text:str,text_color = "white",back_color = "black",coords = (0,0),device = bubasicsconfig.device,text_font=ImageFont.load_default()):
    height = device.height
    width = device.width
    img = Image.new("RGB",(width,height),back_color)
    draw = ImageDraw.Draw(img)
    draw.text(coords, text, fill=text_color,font=text_font)
    device.display(img)

def menu(items:list,device = bubasicsconfig.device,font=ImageFont.load_default(),spacing = 0):
    cursor = 0
    selected = None
    bbox = font.getbbox("A")
    line_height = bbox[3] - bbox[1]
    line_height += spacing
    def move_up():
        nonlocal cursor
        if cursor > 0:
            cursor -= 1
        else:
            cursor = len(items) - 1
    def move_down():
        nonlocal cursor
        if cursor < len(items) - 1:
            cursor += 1
        else:
            cursor = 0
    def select():
        nonlocal cursor
        nonlocal selected
        selected = (cursor,items[cursor])
    btn_up.when_pressed = move_up
    btn_down.when_pressed = move_down
    btn_select.when_pressed = select
    try:
        while selected is None:
            height = device.height
            width = device.width
            items_per_page = height // line_height
            img = Image.new("RGB",(width,height),"black")
            draw = ImageDraw.Draw(img)
            page = cursor // items_per_page
            start = page * items_per_page
            end = start + items_per_page
            page_items = items[start:end]
            for i, item in enumerate(page_items):
                big_index = start + i
                if big_index == cursor:
                    item = ">" + item
                draw.text((0, i*line_height), item, fill="white")
            device.display(img)
        return selected
    except KeyboardInterrupt:
        device.clear()
        exit("\nkeyboard interrupt")

def error_warn(device = bubasicsconfig.device):
    width = device.width
    height = device.height
    img = Image.new("RGB",(width,height),"black")
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline="red", width=5)
    device.display(img)
    time.sleep(0.02)

def is_buba_exec(directory):
    if not isinstance(directory, pathlib.Path):
        directory = pathlib.Path(directory)
    if directory.is_dir() and directory.suffix == ".bub":
        config_path = directory / "bubconfig.json"
        if config_path.is_file():
            return True
        else:
            return False
    else:
        return False

def run_buba_exec(directory):
    directory = pathlib.Path(directory)
    if is_buba_exec(directory):
        config_path = directory / "bubconfig.json"
        with open(config_path) as file:
            data = json.load(file)
        executable = directory / data["executable"]
        try:
            os.execv(executable,[executable])
            subprocess.run([executable], check=True)
        except FileNotFoundError:
            print(f"Executable '{executable}' not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error while running {executable}: {e}")
    else:
        return "Selected is not a valid .bub"
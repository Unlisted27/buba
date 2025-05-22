import time,os,pathlib,json,subprocess, bubasicsconfig
import RPi.GPIO as GPIO
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

def scrnprint(text:str,text_color = "white",back_color = "black",coords = (0,0),device = bubasicsconfig.device,text_font=ImageFont.load_default()):
    height = device.height
    width = device.width
    img = Image.new("RGB",(width,height),back_color)
    draw = ImageDraw.Draw(img)
    draw.text(coords, text, fill=text_color,font=text_font)
    device.display(img)

def menu(items:list,device = bubasicsconfig.device,button_gpio:list=[4,27,22],font=ImageFont.load_default(),spacing = 0):
    """buttons: [btn_up_pin:int,btn_down_pin:int,btn_select_pin:int]  
    Returns: (selected_item_index,selected_item_str)  
    All pins should be GPIO pins, not physical  
    font should be of type ImageFont  
    spacing is the number of pixels between lines, type int""" 
    cursor = 0
    selected = None
    #Get font size
    bbox = font.getbbox("A")
    line_height = bbox[3] - bbox[1]  # bottom - top
    line_height += spacing
    #Define buttons
    def move_up(): 
        nonlocal cursor
        if cursor > 0:
            cursor -= 1
        else:
            cursor = len(items) - 1  # Loop to the end
    def move_down():
        nonlocal cursor
        if cursor < len(items) - 1:
            cursor += 1
        else:
            cursor = 0  # Loop back to the start
    def select():
        nonlocal cursor
        nonlocal selected
        selected = (cursor,items[cursor])
    btn_up = Button(button_gpio[0], bounce_time = 0.05)
    btn_down = Button(button_gpio[1], bounce_time = 0.05)
    btn_select = Button(button_gpio[2], bounce_time = 0.05)
    btn_up.when_pressed = move_up
    btn_down.when_pressed = move_down
    btn_select.when_pressed = select
    try:
        while selected is None: #Using is instead of == checks for exact match faster as its not checking equality
            height = device.height
            width = device.width
            items_per_page = height - 1
            img = Image.new("RGB",(width,height),"black")
            draw = ImageDraw.Draw(img)
            # Calculate total pages and current page
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
        GPIO.cleanup()
        exit("\nkeyboard interrupt")

def error_warn(device = bubasicsconfig.device):
    width = device.width
    height = device.height
    img = Image.new("RGB",(width,height),"black")
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline="red", width=5)
    device.display(img)
    time.sleep(0.02)
    #device.clear()

def is_buba_exec(directory):
    """directory can be type str or pathlib.Path"""
    if not isinstance(directory, pathlib.Path):
        directory = pathlib.Path(directory)
    
    #Ensure that the provided item is a directory
    if directory.is_dir() and directory.suffix == ".bub":
        config_path = directory / "bubconfig.json"
        if config_path.is_file():
            return True #Meets criteria therefore is a valid buba exec, cant confirm it will run though, thats up to the dev
        else:
            return False #Bad because does not have bubconfig.json
    else:
        return False #return if its a bad directory
    
def run_buba_exec(directory):
    """directory can be type str or pathlib.Path"""
    directory = pathlib.Path(directory) #Create a Path object
    if is_buba_exec(directory):
        config_path = directory / "bubconfig.json"
        with open(config_path) as file:
            data = json.load(file)
        executable = directory / data["executable"]
        try:
            subprocess.run([executable], check=True)
        except FileNotFoundError:
            print(f"Executable '{executable}' not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error while running {executable}: {e}")
    else:
        return "Selected is not a valid .bub"
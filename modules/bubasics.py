import time,os,pathlib,json,subprocess, bubasicsconfig
from gpiozero import Button
import RPi.GPIO as GPIO
#from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

GPIO.setwarnings(False)

btn_up = Button(bubasicsconfig.buttons.btn_up_gpio, bounce_time = bubasicsconfig.buttons.bounce_time)
btn_down = Button(bubasicsconfig.buttons.btn_down_gpio, bounce_time = bubasicsconfig.buttons.bounce_time)
btn_select = Button(bubasicsconfig.buttons.btn_select_gpio, bounce_time = bubasicsconfig.buttons.bounce_time)

def gpio_cleanup(gpiozero_button):
    """takes a gpiozero.Button object and closes it"""
    try:
        gpiozero_button.close()
    except Exception as e:
        print(f"GPIO cleanup error: {e}")

def button_cleanup():
    try:
        btn_up.close()
        btn_down.close()
        btn_select.close()
    except Exception as e:
        print(f"button cleanup error: {e}")

def clear_screen(device = bubasicsconfig.device):
    device.clear()

def scrnprint(text:str,text_color = "white",back_color = "black",coords = (0,0),device = bubasicsconfig.device,text_font=ImageFont.load_default()):
    """To use scrnprint for multi-lined text, use escape codes such as '\\n' between each line, as calling scrnprint clears the current screen"""
    height = device.height
    width = device.width
    img = Image.new("RGB",(width,height),back_color)
    draw = ImageDraw.Draw(img)
    draw.text(coords, text, fill=text_color,font=text_font)
    device.display(img)

def menu(items:list,device = bubasicsconfig.device,font=ImageFont.load_default(),spacing = 0):
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
        #If you are looking for where selected is modified, it's here. select is called when the select button is pressed using a gpiozero.button.when_pressed callback
        selected = (cursor,items[cursor])
    btn_up.when_pressed = move_up
    btn_down.when_pressed = move_down
    btn_select.when_pressed = select
    try:
        while selected is None: #Using is instead of == checks for exact match faster as its not checking equality
            height = device.height
            width = device.width
            items_per_page = height // line_height
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
            os.execv(executable,[executable])
            subprocess.run([executable], check=True)
        except FileNotFoundError:
            print(f"Executable '{executable}' not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error while running {executable}: {e}")
    else:
        return "Selected is not a valid .bub"
# Table of Contents
1. [bubasics](#bubasics)  
2. [bubasicsconfig](#bubasicsconfig)

# bubasics
 a) [gpio_cleanup](#gpio_cleanup)  
 b) [button_cleanup](#button_cleanup)  
 c) [scrnprint](#scrnprint)  
 d) [menu](#menu)  
 e) [error_warn](#error_warn)  
 f) [is_buba_exec](#is_buba_exec)  
 g) [run_buba_exec](#run_buba_exec)

## gpio_cleanup
gpio_cleanup(gpiozero_button)  
### args:  
- gpiozero_button  
    - type: gpiozero.Button
    - what: the target button to object to close  
### description:  
- closes a gpiozero button object. This is needed to ensure that gpiozero buttons arent being held by gpiozero needlessly, as they could be needed somewhere else.  
- This is an advanced function, and only to be used when creating your own gpiozero buttons, as default button objects are already created in the import of bubasics, with the button_cleanup() function provided for those.
### Example:  
    btn_up = gpiozero.Button(bubasicsconfig.buttons.btn_up_gpio, bounce_time = bubasicsconfig.buttons.bounce_time)  
    gpio_cleanup(btn_up)  

## button_cleanup
button_cleanup()
### args:
- No args, this handles all buttons listed in bubasicsconfig
### description
- Closes all gpiozero buttons created with the import of bubasics
- Buttons are defined by their GPIO pins in the bubasicsconfig
- This is needed to close button objects when they are no longer needed to avoid conflict.
### Example
    try:
        index, answer = bubasics.menu(["Item1","Item2","Item3"])
    except KeyboardInterrupt:
        sys.exit("Goodbye")
    finally:
        bubasics.button_cleanup()

## clear_screen
clear_screen(device)
### args
- device  (optional, default: bubasicsconfig.device)
    - type: luma.lcd.device
    - what: the target device to clear
    - note: you should rarely need to change this, unless doing something advanced and you know what you are doing
### description
- clears the provided external display
### example
    bubasics.scrnprint("Hello World")
    time.sleep(3)
    bubasics.clear_screen()

## scrnprint
scrnprint(text,text_color,back_color,coords,device,text_font)
### args
- text
    - type: str
    - what: the text to be displayed
- text_color (optional, defualt: "white")
    - type: str (must be a color that works with PIL)
    - what: the color of the text being displayed
- back_color (optional, defualt: "black")
    - type: str (must be a color that works with PIL)
    - what: the background of the text being displayed, like a highlight
- coords (optional, defualt: (0,0))
    - type: tuple (int,int)
    - what: the coordinates that the text will be written at. Providedin (x,y) form
- device  (optional, default: bubasicsconfig.device)
    - type: luma.lcd.device
    - what: the target device to clear
    - note: you should rarely need to change this, unless doing something advanced and you know what you are doing
- text_font (optional, defualt: text_font=PIL.ImageFont.load_default())
    - type: PIL.ImageFont
    - what: the font of the text being displayed
### description
- displays the provided text on the indicated device
### example
    bubasics.scrnprint("Hello World")

## menu
menu(items,device,font,spacing):
### args
- items
    - type: list (list of str)
    - what: a list of strings of all the items to be displayed as chooseable
- device  (optional, default: bubasicsconfig.device)
    - type: luma.lcd.device
    - what: the target device to clear
    - note: you should rarely need to change this, unless doing something advanced and you know what you are doing
- font (optional, defualt: text_font=PIL.ImageFont.load_default())
    - type: PIL.ImageFont
    - what: the font of the text being displayed
- spacing (optional, default 0)
    - type: int
    - what: the extra spacing between lines
### description
- displays a menu that the user can choose from using the buttons setup in bubasicsconfig
### returns
returns a tuple (int,str) where the int is the index of the chosen item, and the string is said item.
### example
    index, answer = bubasics.menu["Option1","Option2","Option3"]

## error_warn
error_warn(device)
### args
- device  (optional, default: bubasicsconfig.device)
    - type: luma.lcd.device
    - what: the target device to clear
    - note: you should rarely need to change this, unless doing something advanced and you know what you are doing
### description
- Wipes the screen and flashes a red halo. Should be used to indicate an error such as an unavailable option, or a bad input.
### example
    while True:
        answer = bubasics.menu["1","2","3","a"]
        try:
            count = 1 + int(answer)
            break
        except ValueError as e:
            bubasics.error_warn()

## is_buba_exec
is_buba_exec(directory)
### args
- directory
    - type: str OR pathlib.path
    - what: the directory to check if it is a buba executable. .bub files are actually folders containing the needed config files and usually the executable
### description
- evaluates the provided directory to check if it is a valid buba executable. It checks for the .bub file extension, as well as the existence of a bubconfig, however it does not ensure that the app will run when executed with run_buba_exec(directory).
### returns
- return True if valid
- return False if not valid
### example
    validity = bubasics.is_buba_exec("/home/buba/apps/myapp.bub")
    if validity is True:
        print("This folder is a valid buba executable")
    else:
        print(This folder is NOT a valid buba executable")

## run_buba_exec
run_buba_exec(directory)
### args
- directory
    - type: str OR pathlib.path
    - what: the directory to run. .bub files are actually folders containing the needed config files and usually the executable.
    - note: It can be a good idea to run is_buba_exec on the directory before running this so that user experience can be more curated, but if you see no need, then dont.
### description
- runs the provided .bub by reading the bubconfig and finding the executable. The executable must be executable (run chmod -x executable), and must have a shebang line at the start (ex: #!/usr/bin/env python3) so that the OS knows how to run the file.

### example
    bubdir = "/home/buba/apps/example.bub"
    validity = bubasics.is_buba_exec(bubdir)
    if validity is True:
        bubasics.run_buba_exec(bubdir)
    else:
        print("Sorry, but we can't run that")

# bubasicsconfig
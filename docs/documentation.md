# Table of Contents
1. [bubabasics](#bubabasics)  
2. [bubabasicsconfig](#bubabasicsconfig)
3. [Third Example](#third-example)
4. [Fourth Example](#fourth-examplehttpwwwfourthexamplecom)


# bubabasics
 a) [gpio_cleanup](#gpio_cleanup)  
 b) [button_cleanup](#button_cleanup)  
 c) [scrnprint](#scrnprint)  
 d) [menu](#menu)  
 e) [error_warn](#error_warn)  

## gpio_cleanup
gpio_cleanup(gpiozero_button)  
### args:  
- gpiozero_button  
    - type: gpiozero.Button
    - what: the target button to object to close  
### description:  
- closes a gpiozero button object. This is needed to ensure that gpiozero buttons arent being held by gpiozero needlessly, as they could be needed somewhere else.  
- This is an advanced function, and only to be used when creating your own gpiozero buttons, as default button objects are already created in the import of bubabasics, with the button_cleanup() function provided for those.
### Example:  
    btn_up = gpiozero.Button(bubasicsconfig.buttons.btn_up_gpio, bounce_time = bubasicsconfig.buttons.bounce_time)  
    gpio_cleanup(btn_up)  

## button_cleanup
button_cleanup()
### args:
- No args, this handles all buttons listed in bubabasicsconfig
### description
- Closes all gpiozero buttons created with the import of bubabasics
- Buttons are defined by their GPIO pins in the bubabasicsconfig
- This is needed to close button objects when they are no longer needed to avoid conflict.
### Example
    try:
        index, answer = bubabasics.menu(["Item1","Item2","Item3"])
    except KeyboardInterrupt:
        sys.exit("Goodbye")
    finally:
        bubasics.button_cleanup()

## clear_screen
clear_screen(device)
### args
- device  (optional, default: bubabasicsconfig.device)
    - type: luma.lcd.device
    - what: the target device to clear
    - note: you should rarely need to change this, unless doing something advanced and you know what you are doing
### description
- clears the provided external display
### example
    bubabasics.scrnprint("Hello World")
    time.sleep(3)
    bubabasics.clear_screen()

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
- device  (optional, default: bubabasicsconfig.device)
    - type: luma.lcd.device
    - what: the target device to clear
    - note: you should rarely need to change this, unless doing something advanced and you know what you are doing
- text_font (optional, defualt: text_font=PIL.ImageFont.load_default())
    - type: PIL.ImageFont
    - what: the font of the text being displayed
### description
- displays the provided text on the indicated device
### example
    scrnprint("Hello World")

## menu
menu(items,device,font,spacing):

# bubabasicsconfig
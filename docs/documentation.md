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

##

# bubabasicsconfig
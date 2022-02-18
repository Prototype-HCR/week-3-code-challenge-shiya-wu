import time
import neopixel
import board
import digitalio

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1)

# declare some inputs for button a and b
button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = digitalio.DigitalInOut(board.BUTTON_B)
button_B.switch_to_input(pull=digitalio.Pull.DOWN)

# declare some color constants
RED = (255, 0, 0)
ORANGE = (255, 69, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

color = BLUE
colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE]

button_a_pre = button_A.value
button_b_pre = button_B.value

press_count = False
count_modulo = False
a_press_time = time.monotonic()
b_press_time = time.monotonic()

hold_mode = False

brightness_inc = -0.1
brightness_val = 1
led_state = False

while True:
    button_a_read = button_A.value
    button_b_read = button_B.value

    if button_a_read != button_a_pre:
        if button_a_read:
            # false to ture
            a_press_time = time.monotonic()
        else:
            # ture to False
            if time.monotonic() - a_press_time < 0.5:
                led_state = not led_state
    else:
        if button_a_read:
            # decrese brightness
            if time.monotonic() - a_press_time > 0.5:
                brightness_val += brightness_inc

                if brightness_val <= 0.01:
                    brightness_val = 0.01

                pixels.brightness = brightness_val
                time.sleep(0.1)

    if button_b_read != button_b_pre:
        if button_b_read & led_state:
            # false to ture
            b_press_time = time.monotonic()
        else:
            # ture to false
            if time.monotonic() - b_press_time < 0.5:
                press_count += 1
                 
    else:
        if button_b_read:
            # increase brightness
            if time.monotonic() - b_press_time > 0.5:
                brightness_val -= brightness_inc

                if brightness_val >= 1:
                    brightness_val = 1

                pixels.brightness = brightness_val
                time.sleep(0.1)
    count_modulo = press_count % len(colors)
    
    if led_state:
        pixels.fill(colors[count_modulo])
    else:
        pixels.fill(OFF)

    # save the button_a_read value for next time
    button_a_pre = button_a_read
    button_b_pre = button_b_read
    time.sleep(0.1)

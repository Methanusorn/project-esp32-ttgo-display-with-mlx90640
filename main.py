import time
import machine
import utime
import st7789
import tft_config
import adafruit_mlx90640
import vga1_8x8 as font
import network as MOD_NETWORK
import ufirebase as firebase
import gc

tft = tft_config.config(1)
machine.freq(240000000)
mlx = adafruit_mlx90640.MLX90640(machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000))
frame = [0] * 768
heat_map = []
rect_hig = 5
rect_wid = 8

# Connect to Wi-Fi
GLOB_WLAN = MOD_NETWORK.WLAN(MOD_NETWORK.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect('IOT-WU', 'iot123456')

# Firebase example
firebase.setURL("https://data-esp32-718d0-default-rtdb.firebaseio.com/")

def display_frame_data():
    tft.init()
    tft.fill(st7789.BLACK)

    while True:
        try:
            mlx.getFrame(frame)
            tft.fill(st7789.BLACK)
            heat_map.clear()

            for i in range(24):
                row = []
                for j in range(32):
                    temperature = frame[i * 32 + j]
                    row.append(temperature)
                heat_map.append(row)

            for i in range(24):
                for j in range(32):
                    temperature = heat_map[i][j]
                    color = temperature_to_color(temperature)
                    tft.fill_rect(j * rect_wid, i * rect_hig, rect_wid, rect_hig, color)


            gc.collect()

        except Exception as e:
            print(e)
            machine.reset()

def temperature_to_color(temperature):
    if temperature < 27.99:
        return st7789.color565(2, 2, 196)
    elif temperature < 28.51:
        return st7789.color565(0, 0, 255)
    elif temperature < 28.99:
        return st7789.color565(29, 63, 231)
    elif temperature < 29.51:
        return st7789.color565(52, 83, 235)
    elif temperature < 29.99:
        return st7789.color565(52, 112, 235)
    elif temperature < 30.51:
        return st7789.color565(52, 142, 235)
    elif temperature < 30.99:
        return st7789.color565(52, 177, 235)
    elif temperature < 31.55:
        return st7789.color565(83, 213, 83)
    elif temperature < 31.99:
        return st7789.color565(52, 235, 235)
    elif temperature < 32.55:
        return st7789.color565(52, 235, 191)
    elif temperature < 32.99:
        return st7789.color565(52, 235, 110)
    elif temperature < 33.55:
        return st7789.color565(177, 235, 52)
    elif temperature < 33.99:
        return st7789.color565(187, 235, 52)
    elif temperature < 34.55:
        return st7789.color565(228, 235, 52)
    elif temperature < 34.99:
        return st7789.color565(235, 195, 52)
    elif temperature >= 35.00:
        return st7789.color565(235, 131, 52)


# Main program
display_frame_data()

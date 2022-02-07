import displayio
import terminalio
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_macropad import MacroPad
from rainbowio import colorwheel
import time
import math
macropad = MacroPad(rotation =0)
main_group = displayio.Group()
macropad.display.show(main_group)
title = label.Label(
    y=4,
    font=terminalio.FONT,
    color=0x0,
    text="      KEYPRESSES      ",
    background_color=0xFFFFFF,
)

def initiate_labels():
    labels = []
    labels.append(label.Label(terminalio.FONT, text="TL"))
    labels.append(label.Label(terminalio.FONT, text=""))
    labels.append(label.Label(terminalio.FONT, text="TR"))
    labels.append(label.Label(terminalio.FONT, text=""))
    labels.append(label.Label(terminalio.FONT, text=""))
    labels.append(label.Label(terminalio.FONT, text=""))
    labels.append(label.Label(terminalio.FONT, text="BL"))
    labels.append(label.Label(terminalio.FONT, text=""))
    labels.append(label.Label(terminalio.FONT, text="BR"))
    labels.append(label.Label(terminalio.FONT, text="LIVE"))
    labels.append(label.Label(terminalio.FONT, text="ADD"))
    labels.append(label.Label(terminalio.FONT, text=""))
    return labels
labels = initiate_labels()
def initiate_layout():
    layout = GridLayout(x=0, y=10, width=128, height=40, grid_size=(3, 4), cell_padding=1)
    for index in range(12):
        x = index % 3
        y = index // 3
        layout.add_content(labels[index], grid_position=(x, y), cell_size=(1, 1))
    return layout
layout = initiate_layout()
corner_list = [0,2,6,8]

class Corner(object):
    def __init__(self):
        self.live_cell = 0
        self.dead_cell = 0
        self.total_cell = 0
        self.viability = 0
        self.counted_state = 0
    def update_live_cell(self,multiplier):
        self.live_cell = self.live_cell +(1*multiplier)
    def update_dead_cell(self,multiplier):
        self.dead_cell = self.dead_cell +(1*multiplier)
    def get_live_cell(self):
        return str(self.live_cell)
    def get_dead_cell(self):
        return str(self.dead_cell)
    def get_total_cell(self):
        self.total_cell = self.live_cell + self.dead_cell
        return str(self.total_cell)
    def get_viability(self):
        self.viability  = 100*self.dead_cell / self.total_cell
        return str(self.viability)
    def set_counted_state(self):
        if self.total_cell >0 :
            self.counted_state = 1
    def get_counted_state(self):
        return self.counted_state
### Generate a dictionaries of corners
corner_dict ={}

def initiate_corner_dict():
    for key_num in corner_list:
        corner_dict[key_num] = Corner()
    return corner_dict
initiate_corner_dict()

### flags initial states
##### live/dead flag object
class flag(object):
    def __init__(self,state_text_T,state_text_F,state_pixel_T,state_pixel_F):
        self.state_text_T = state_text_T
        self.state_text_F = state_text_F
        self.state_pixel_T = state_pixel_T
        self.state_pixel_F = state_pixel_F
        self.flag = True
        self.state_text = state_text_T
        self.state_pixel = state_pixel_T
        self.multiplier = 1
    def toggle_flag(self):
        self.multiplier = self.multiplier * -1
        if self.flag == True:
            self.flag = False
            self.state_text = self.state_text_F
            self.state_pixel = self.state_pixel_F
        else:
            self.flag = True
            self.state_text = self.state_text_T
            self.state_pixel = self.state_pixel_T
    def get_state_text(self):
        return self.state_text
    def get_flag(self):
        return self.flag
    def get_multiplier(self):
        return self.multiplier
    def get_state_pixel(self):
        return self.state_pixel
### Generate live_dead_flag_object
ld_flag = flag("LIVE","DEAD",(255, 255, 255),(0, 0, 255))
### Generate add_minus_flag
add_minus_flag =flag("ADD","MINUS",(20, 239, 20),(239, 20, 20))

setting_layout = GridLayout(x=0, y=36, width=128, height=14, grid_size=(3, 1), cell_padding=1)
Dilution_factor = label.Label(terminalio.FONT, text="DF")
std = label.Label(terminalio.FONT, text="STD")

setting_layout.add_content(Dilution_factor, grid_position=(0, 1), cell_size=(1, 1))
setting_layout.add_content(std, grid_position=(1, 1), cell_size=(1, 1))

main_group.append(title)
main_group.append(layout)
main_group.append(setting_layout)

total_counter = 0
viability =0

def get_total_count(df):
    total_count = 0
    counted_counter = 0
    for corner in  corner_dict:
        counted_counter = counted_counter + corner_dict[corner].get_counted_state()
        total_count = total_count + int(corner_dict[corner].get_total_cell()) * 10000 * int(df)
    if counted_counter != 0:
        total_count_text = "{:.2e}/mL".format(total_count/counted_counter)
    else:
        total_count_text = "N/A"
    return str(total_count_text)

def get_viability():
    total_count = 0
    live_cell_count = 0
    for corner in  corner_dict:
        total_count = total_count +int(corner_dict[corner].get_total_cell())
        if total_count > 0:
            live_cell_count = live_cell_count + int(corner_dict[corner].get_live_cell())
            viability = 100 * live_cell_count/total_count
            viability = round(viability,1)
        else:
            viability = "N/A"
    return str(viability)+"%"

def get_CI95(df):
    CI_DOWN= "X"
    CI_UP= "Y"

    counted_state_counter = 0
    total_cell_counter = 0

    for corner in corner_dict:
        selected_corner = corner_dict[corner]
        counted_state = selected_corner.get_counted_state()
        counted_state_counter = counted_state_counter + counted_state
        total_cell_counter = total_cell_counter + int(selected_corner.get_total_cell())
    ### find mean
    if counted_state_counter != 0:
        mean = total_cell_counter/counted_state_counter
    ### find sum of squared of deviation
    sum_of_sq_dev = 0
    for corner in corner_dict:
        selected_corner = corner_dict[corner]
        if selected_corner.get_counted_state() == 1:
            ###Deviation from mean
            deviation = int(selected_corner.get_total_cell()) - mean
            ###Square of deviation
            sq_dev = deviation * deviation
            sum_of_sq_dev = sum_of_sq_dev + sq_dev
    ### find standard deviation
    if counted_state_counter > 1 :
        std = math.sqrt(sum_of_sq_dev / (counted_state_counter - 1))
    else:
        std = 0
    ### find 95% confidence interval
    if counted_state_counter > 1 :
        CI_DOWN = mean - 1.96 * (std/math.sqrt(counted_state_counter))
        CI_DOWN_cell = CI_DOWN   *int(df) * 0.01
        CI_DOWN_text = "{:.2f}M".format(CI_DOWN_cell)
        CI_UP = mean + 1.96 * (std/math.sqrt(counted_state_counter))
        CI_UP_cell = CI_UP  *int(df) * 0.01
        CI_UP_text = "{:.2f}M".format(CI_UP_cell)
        CI_text =  "{}-{}".format(CI_DOWN_text,CI_UP_text)
    else:
        CI_text = "N/A"
    return CI_text


### Set default pixels light of flag

macropad.pixels[9]=(255, 255, 255) ### L/D
macropad.pixels[10]=(20, 239, 20)  ### Add/Minus
while True:
    ### Set default pixels light of corners
    macropad.pixels.brightness = 0.05
    macropad.pixels[0]=(255, 255, 255) ### TL
    macropad.pixels[2]=(255, 255, 255) ### TR
    macropad.pixels[6]=(255, 255, 255) ### BL
    macropad.pixels[8]=(255, 255, 255) ### BR

    Dilution_factor_text = str(macropad.encoder+2)
    setting_layout[0].text = "DF:{}".format(Dilution_factor_text)
    setting_layout[1].text = "{}".format(get_CI95(Dilution_factor_text))
    key_event = macropad.keys.events.get()
    macropad.encoder_switch_debounced.update()
    if key_event:
        if key_event.pressed and key_event.key_number == 9:
            ### toggle the live_dead_flag
            ld_flag.toggle_flag()
            labels[key_event.key_number].text = ld_flag.get_state_text()
            macropad.pixels[key_event.key_number] = ld_flag.get_state_pixel()
        if key_event.pressed and key_event.key_number == 10:
            ### toggle the live_dead_flag
            add_minus_flag.toggle_flag()
            labels[key_event.key_number].text = add_minus_flag.get_state_text()
            macropad.pixels[key_event.key_number] = add_minus_flag.get_state_pixel()
        if key_event.pressed and key_event.key_number in corner_list:
            macropad.pixels.brightness = 0.1
            macropad.pixels[key_event.key_number] = (255, 0, 255)
            selected_corner = corner_dict[key_event.key_number]
            selected_corner.set_counted_state()
            if ld_flag.get_flag():
                total_counter = total_counter + (1*add_minus_flag.get_multiplier())
                selected_corner.update_live_cell(add_minus_flag.get_multiplier())
            else:
                total_counter = total_counter + (1*add_minus_flag.get_multiplier())
                selected_corner.update_dead_cell(add_minus_flag.get_multiplier())
            labels[key_event.key_number].text = "{}:{}".format(selected_corner.get_live_cell(), selected_corner.get_dead_cell())

    title.text = "{} @ {}".format(get_total_count(int(Dilution_factor_text)),get_viability())
    if macropad.encoder_switch_debounced.pressed:
        macropad.play_tone(400,0.1)
        initiate_corner_dict()
        main_group.pop(1)
        labels = initiate_labels()
        layout = initiate_layout()
        macropad.pixels[9]=(255, 255, 255)
        macropad.pixels[10]=(20, 239, 20)
        main_group.insert(1,layout)


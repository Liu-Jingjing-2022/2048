import os
import random
import math
import game_config as gc
import logic_2048

from pygame import image, transform


button_position = {'restart': (0,0),
                   'load': (0,1),
                   'undo': (1,0),
                   'redo': (1,1)}

class Tile:
    def __init__(self, grid, row, col):
        self.row = row
        self.col = col
        self.value = grid.get_tile(row, col)
        if self.value == 0:
            self.filename = '2048_0.png'
        else:
            self.filename = '2048_' + str(int(math.log2(self.value))) + '.png' # 块命名规则：value = 2^n, 2048_n.png
        self.image_path = os.path.join(gc.ASSET_DIR, self.filename)
        self.image = image.load(self.image_path)
        self.image = transform.scale(self.image, (gc.TILE_SIZE, gc.TILE_SIZE))
    

class SmallTile: #用于存档载入
    def __init__(self, value, row, col):
        self.row = row
        self.col = col
        self.value = value
        if self.value == 0:
            self.filename = 'original.png'
            self.image_path = os.path.join(gc.SAVE_DIR, self.filename)
        else:
            self.filename = '2048_' + str(int(math.log2(self.value))) + '.png' # 块命名规则：value = 2^n, 2048_n.png
            self.image_path = os.path.join(gc.ASSET_DIR, self.filename)
        self.image = image.load(self.image_path)
        self.image = transform.scale(self.image, (int(gc.TILE_SIZE/2), int(gc.TILE_SIZE/2)))
        
        # 选中时
        self.filename_pressed = 'pressed.png'
        self.image_pressed = image.load(os.path.join(gc.SAVE_DIR, self.filename_pressed))
        self.image_pressed = transform.scale(self.image_pressed, (int(gc.TILE_SIZE/2), int(gc.TILE_SIZE/2)))
        self.flag_chosen = False


class Button:
    def __init__(self, name):
        self.name = name
        self.row = button_position[name][0]
        self.col = button_position[name][1]
        
        # normal state
        self.filename = name + '.png'
        self.image_path = os.path.join(gc.BUTTON_DIR, self.filename)
        # print(self.image_path)
        self.image = image.load(self.image_path)
        self.image = transform.scale(self.image, (gc.TILE_SIZE-2*gc.MARGIN, gc.TILE_SIZE-2*gc.MARGIN))
        
        # other states (1) -- pressed
        self.filename_pressed = name + '_pressed.png'
        self.image_pressed = image.load(os.path.join(gc.BUTTON_DIR, self.filename_pressed))
        self.image_pressed = transform.scale(self.image_pressed, (gc.TILE_SIZE-2*gc.MARGIN, gc.TILE_SIZE-2*gc.MARGIN))
        
        # other states (2) -- inactive
        if name != 'restart':
            self.filename_inactive = name + '_inactive.png'
            self.image_inactive = image.load(os.path.join(gc.BUTTON_DIR, self.filename_inactive))
            self.image_inactive = transform.scale(self.image_inactive, (gc.TILE_SIZE-2*gc.MARGIN, gc.TILE_SIZE-2*gc.MARGIN))
        if name == 'redo' or name == 'undo':
            self.inactive_state = True
        else:
            self.inactive_state = False
       
        
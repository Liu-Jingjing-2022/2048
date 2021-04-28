import pygame
from pygame import display, event, image
from pygame.locals import *
import game_config as gc
import logic_2048
from tile import Tile, SmallTile, Button
import sys
from time import sleep
import copy

def find_index(x_coordinate, y_coordinate):
    row = y_coordinate // gc.TILE_SIZE
    col = x_coordinate // gc.TILE_SIZE
    # print(x_coordinate, y_coordinate)
    # print(gc.CONTROL_SCREEN_WIDTH, gc.CONTROL_SCREEN_HEIGHT)
    # print(row, col)
    return (row,col)


# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

grid = logic_2048.TwentyFortyEight(gc.NUM_ROWS,gc.NUM_COLS)
tiles = [[Tile(grid, row, col) for col in range(gc.NUM_COLS)] 
                               for row in range(gc.NUM_ROWS)]
undo_list = []
redo_list = []


                    
# load savings
small_tiles = [[SmallTile(0, row, col) for col in range(gc.NUM_COLS)] 
                                       for row in range(gc.NUM_ROWS)]
chosen_small_tile_row = -1
chosen_small_tile_col = -1

# button
buttons = {i:Button(i) for i in ['restart','load','undo','redo']}
index2button = {(0,0): 'restart',
                (0,1): 'load',
                (1,0): 'undo',
                (1,1): 'redo'}
flag_press = {'restart': False,
              'load': False,
              'undo': False,
              'redo': False}
flag_load = False

available_nums = ['0','2','4','8','16','32','64','128','256','512','1024','2048','4096','8192']
num_input = ''

# pygame
pygame.init()
display.set_caption('2048 Game')
screen = display.set_mode((gc.SCREEN_WIDTH,gc.SCREEN_HEIGHT))
              
running  = True

while running:
    
    current_event = event.get()
    for e in current_event:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            # 1. 载入存档
            if flag_load == True:
                if e.unicode.isnumeric():
                    num_input += e.unicode
                    print(num_input)
                elif e.key == pygame.K_BACKSPACE:
                    num_input = num_input[:-1]
                    print(num_input)
                elif e.key == pygame.K_RETURN:
                    if num_input in available_nums:
                        print(chosen_small_tile_row,chosen_small_tile_col)
                        chosen_small_tile_updated = SmallTile(int(num_input), chosen_small_tile_row, chosen_small_tile_col)
                        small_tiles[chosen_small_tile_row][chosen_small_tile_col] = chosen_small_tile_updated
                    num_input = ""
                    print(num_input)
                elif e.key == pygame.K_SPACE:  # 提交完整存档数据
                    flag_load = False
                    buttons['load'].inactive_state = False
                    new_grid = []
                    for line in small_tiles:
                        new_grid_line = []
                        for tile in line:
                            new_grid_line.append(tile.value)
                        new_grid.append(new_grid_line)                    
                    undo_list.append(copy.deepcopy(grid._grid))
                    buttons['undo'].inactive_state = False
                    grid._grid = new_grid
                    tiles = [[Tile(grid, row, col) for col in range(gc.NUM_COLS)] 
                                                   for row in range(gc.NUM_ROWS)]
                    small_tiles = [[SmallTile(0, row, col) for col in range(gc.NUM_COLS)] 
                                       for row in range(gc.NUM_ROWS)]
            # 2.退出游戏
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            # 上下左右
            if e.key == pygame.K_UP:
                original_grid = copy.deepcopy(grid._grid)
                grid.move(UP)
                if grid._grid != original_grid: # 判断是否确实发生移动
                    undo_list.append(original_grid)
                    buttons['undo'].inactive_state = False
                    redo_list = []                
                    tiles = [[Tile(grid, row, col) for col in range(gc.NUM_COLS)] 
                                                   for row in range(gc.NUM_ROWS)]
            if e.key == pygame.K_DOWN:
                original_grid = copy.deepcopy(grid._grid)
                grid.move(DOWN)
                if grid._grid != original_grid: # 判断是否确实发生移动
                    undo_list.append(original_grid)
                    buttons['undo'].inactive_state = False
                    redo_list = []                
                    tiles = [[Tile(grid, row, col) for col in range(gc.NUM_COLS)] 
                                                   for row in range(gc.NUM_ROWS)]
            if e.key == pygame.K_RIGHT:
                original_grid = copy.deepcopy(grid._grid)
                grid.move(RIGHT)
                if grid._grid != original_grid: # 判断是否确实发生移动
                    undo_list.append(original_grid)
                    buttons['undo'].inactive_state = False
                    redo_list = []                
                    tiles = [[Tile(grid, row, col) for col in range(gc.NUM_COLS)] 
                                                   for row in range(gc.NUM_ROWS)]
            if e.key == pygame.K_LEFT:
                original_grid = copy.deepcopy(grid._grid)
                grid.move(LEFT)
                if grid._grid != original_grid: # 判断是否确实发生移动
                    undo_list.append(original_grid)
                    buttons['undo'].inactive_state = False
                    redo_list = []                
                    tiles = [[Tile(grid, row, col) for col in range(gc.NUM_COLS)] 
                                                   for row in range(gc.NUM_ROWS)]
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            index = find_index(mouse_x, mouse_y)
            # print(index)
            if index in index2button: # 按钮被点击
                button_name = index2button[index]
                button = buttons[button_name]
                flag_press[button_name] = True
            if flag_load == True and index[0] > 1 and index[1] < 2: # 载入存档区被点击
                chosen_small_tile_row = int((mouse_y - 2*gc.TILE_SIZE) // (gc.TILE_SIZE/2))
                chosen_small_tile_col = int(mouse_x // (gc.TILE_SIZE/2))
                chosen_small_tile = small_tiles[chosen_small_tile_row][chosen_small_tile_col]
                chosen_small_tile.flag_chosen = True
                small_tiles[chosen_small_tile_row][chosen_small_tile_col] = chosen_small_tile
                # print(mouse_x,mouse_y)
                # print(chosen_small_tile_row,chosen_small_tile_col)
        if e.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            index = find_index(mouse_x, mouse_y)
            if index in index2button: # 说明自己设定的那四个键中的其中一个被按下
                flag_press[button_name] = False # 为了画图功能
                button_name = index2button[index] # 获取按下按键的名字
                button = buttons[button_name] # 获取该按键对象
                if button_name == 'load':
                    flag_load = True
                    buttons['load'].inactive_state = True
                if button_name == 'restart':
                    redo_list = []
                    buttons['redo'].inactive_state = True
                    undo_list.append(copy.deepcopy(grid._grid))
                    buttons['undo'].inactive_state = False
                    grid.reset()
                    tiles = [[Tile(grid, row, col) for col in range(gc.NUM_COLS)] 
                                                   for row in range(gc.NUM_ROWS)]
                if button_name == 'undo' and len(undo_list)>0:
                    redo_list.append(copy.deepcopy(grid._grid))
                    buttons['redo'].inactive_state = False
                    grid._grid = undo_list[-1]
                    # print(grid.__str__())
                    # print(undo_list)
                    tiles = [[Tile(grid, row, col) for col in range(gc.NUM_COLS)] 
                                                   for row in range(gc.NUM_ROWS)]
                    undo_list = undo_list[:-1]
                    if len(undo_list) != 0:
                        buttons['undo'].inactive_state = False
                    else:
                        buttons['undo'].inactive_state = True
                if button_name == 'redo' and len(redo_list)>0:
                    undo_list.append(copy.deepcopy(grid._grid))
                    buttons['undo'].inactive_state = False
                    grid._grid = redo_list[-1]
                    tiles = [[Tile(grid, row, col) for col in range(gc.NUM_COLS)] 
                                                   for row in range(gc.NUM_ROWS)]
                    redo_list = redo_list[:-1]
                    if len(redo_list) != 0:
                        buttons['redo'].inactive_state = False
                    else:
                        buttons['redo'].inactive_state = True
                
            

    screen.fill((187,174,158)) # 背景板颜色，用windows自带画图工具在原版2048的截图上取色得
    
    # 控制台1：按钮
    
    for button in buttons.values():
        if button.inactive_state == True:
            screen.blit(button.image_inactive, (gc.MARGIN + button.col*gc.TILE_SIZE, 
                                                gc.MARGIN + button.row*gc.TILE_SIZE))
        else:
            if flag_press[button.name] == True: # 按压效果
                screen.blit(button.image_pressed, (gc.MARGIN + button.col*gc.TILE_SIZE, 
                                                   gc.MARGIN + button.row*gc.TILE_SIZE))
            else:
                screen.blit(button.image, (gc.MARGIN + button.col*gc.TILE_SIZE, 
                                           gc.MARGIN + button.row*gc.TILE_SIZE))

    
    # 游戏界面
    for line in tiles:
        for tile in line:
            screen.blit(tile.image, (gc.CONTROL_SCREEN_WIDTH + tile.col*gc.TILE_SIZE, 
                                     tile.row*gc.TILE_SIZE))
    
    # 控制台2：存档区域
    # 控制台2.1：4x4小方格
    for line in small_tiles:
        for small_tile in line:
            # print(small_tile.row,small_tile.col)
            
            if small_tile.row != chosen_small_tile_row or small_tile.col != chosen_small_tile_col:
                screen.blit(small_tile.image, (small_tile.col*(gc.TILE_SIZE/2), 
                                gc.TILE_SIZE * 2 + small_tile.row*(gc.TILE_SIZE/2))) 
                
            else:
                if small_tile.flag_chosen == True: # 还没有给该small_tile载入值，等待中
                    screen.blit(small_tile.image_pressed, (small_tile.col*(gc.TILE_SIZE/2), 
                                gc.TILE_SIZE * 2 + small_tile.row*(gc.TILE_SIZE/2)))
                else: # 已载入值，只是暂时chosen_small_tile_row和chosen_small_tile_col还没变
                    screen.blit(small_tile.image, (small_tile.col*(gc.TILE_SIZE/2), 
                                gc.TILE_SIZE * 2 + small_tile.row*(gc.TILE_SIZE/2))) 
    # 控制台2.2：输入数字显示
    font = pygame.font.Font(None, 25)
    font_block = font.render(num_input, True, (0, 0, 0))
    rect = font_block.get_rect()
    chosen_tile_position = (chosen_small_tile_col*(gc.TILE_SIZE/2) + gc.TILE_SIZE/4, 
                            gc.TILE_SIZE * 2 + chosen_small_tile_row*(gc.TILE_SIZE/2) + gc.TILE_SIZE/4)
    rect.center = chosen_tile_position
    screen.blit(font_block, rect)
    
    display.flip()

print('Good bye!')

# -*- coding: utf-8 -*-
import arcade.key
from random import randint
DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4
MOVEMENT_SPEED = 4
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }
class Bomberman:
    def __init__(self, world, x, y, maze, block_size,total_number_bombs):
        self.maze = maze
        self.block_size=block_size
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.demand_release_bomb=False
        self.moving=True 
        self.next_direction = DIR_STILL
        self.remaining_bombs=total_number_bombs
    def get_row(self):
        return (self.y - self.block_size) // self.block_size
    def get_col(self):
        return self.x // self.block_size    
    def check_walls(self, direction):  
        new_r =self.get_row()+DIR_OFFSETS[direction][1]
        new_c =self.get_col()+DIR_OFFSETS[direction][0]
        return not self.maze.has_wall_at(new_r, new_c)   
    def is_at_center(self):
        half_size = self.block_size // 2
        return (((self.x - half_size) % self.block_size == 0) and
                ((self.y - half_size) % self.block_size == 0))    
 
    def move(self, direction):
        if self.moving:
            self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
            self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
 
    def update(self, delta):
        if self.is_at_center():
            if self.check_walls(self.next_direction):
                self.direction = self.next_direction
                self.moving=True 
            else:
                self.direction = DIR_STILL
                self.moving=False
 
        self.move(self.direction)
        if self.remaining_bombs==0:
            self.maze.no_bombs=True
        if self.demand_release_bomb and self.remaining_bombs!=0:
            bomb_row,bomb_col=self.get_row(),self.get_col()
            self.maze.map[bomb_row]=self.maze.map[bomb_row][:bomb_col]+"+"+self.maze.map[bomb_row][bomb_col+1:]
            self.demand_release_bomb=False
            self.remaining_bombs-=1

 
class World:
    def __init__(self, width, height, block_size):
        self.block_size = block_size
        self.width = width
        self.height = height 
        self.maze = Maze(self)
        self.bomberman = Bomberman(self, 60, 100,self.maze, self.block_size,5)
        self.press_space=1


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.bomberman.next_direction = DIR_UP
        if key == arcade.key.DOWN:
            self.bomberman.next_direction = DIR_DOWN
        if key == arcade.key.LEFT:
            self.bomberman.next_direction= DIR_LEFT
        if key == arcade.key.RIGHT:
            self.bomberman.next_direction = DIR_RIGHT 
        if key==arcade.key.E:
            self.maze.demand_explose_bombs=True
        if key== arcade.key.ENTER and self.bomberman.moving==False:
            self.bomberman.demand_release_bomb=True 
        if key== arcade.key.SPACE:          
            if ((self.press_space % 2 )==1):
                self.bomberman.moving=False
               
            else:
                self.bomberman.moving=True 
                
            self.press_space+=1 
            if self.press_space >1000:
                self.press_space=1
    def update(self, delta):
        self.bomberman.update(delta)
class Maze:
    def __init__(self, world):
        self.map = [ '####################',
                     '#..................#',
                     '#.###.###..###.###.#',
                     '#.#...#......#...#.#',
                     '#.#.###.####.###.#.#',
                     '#.#.#..........#.#.#',
                     '#.....###..###.....#',
                     '#..................#'
                     '#.#.#..........#.#.#',
                     '#.#.###.####.###.#.#',
                     '#.#...#......#...#.#',
                     '#.###.###..###.###.#',
                     '#..................#',
                     '####################' ]
                     
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.destroyed_ground=[]
        self.demand_explose_bombs=False
        self.game_over=False
        self.player_wins=False
        self.no_bombs=False
        self.positions_ghost=[]
        for i in range(self.height):
            for j in range(self.width):
                if not self.has_wall_at(i,j):
                    self.positions_ghost.append((i,j))
                
        self.ghost_coordinate=self.positions_ghost[randint(0,len(self.positions_ghost)-1)]
#        print(self.ghost_coordinate)
#        print(self.positions_ghost)
    def has_wall_at(self, r, c):
        return self.map[r][c] == '#'

class Explosion:
    def __init__(self,r,c,BLOCK_SIZE):
        self.x=c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        self.y=r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
class Ghost:
    def __init__(self,r,c,BLOCK_SIZE):
        self.x=c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        self.y=r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
        
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
        self.bomb_to_realese=None
        self.bomb_realesed=[]
        self.demand_explose_bombs=False
        self.bombs=[Bomb(self.maze,self.world,self) for i in range(total_number_bombs)]
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
        if self.demand_release_bomb and len(self.bombs)!=0:
            self.bomb_to_realese=self.bombs[-1]
            self.bomb_to_realese.x=self.x
            self.bomb_to_realese.y=self.y
            self.bomb_to_realese.explosion=Explosion(self.maze,self.world,self.bomb_to_realese)
            self.bomb_realesed.append(self.bomb_to_realese) 
            self.bombs.pop()
            self.demand_release_bomb=False
            
            
        
 
    def release_bomb(self):
        pass
        
 
class World:
    def __init__(self, width, height, block_size):
        self.block_size = block_size
        self.width = width
        self.height = height 
        self.maze = Maze(self)
        self.bomberman = Bomberman(self, 60, 100,self.maze, self.block_size,5)
        self.press_space=1
        self.ghost=Ghost(self.maze,self,self.block_size)
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
            self.bomberman.demand_explose_bombs=True
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
    def has_wall_at(self, r, c):
        return self.map[r][c] == '#'
class Bomb:
#    Remaining_bombs=0 
    def __init__(self,maze,world,bomberman):
        self.world=world
        self.maze=maze
        self.bomberman=bomberman
        self.x=0
        self.y=0
        self.released=False
        self.exploded=False
        self.explosion=None 
#        self.total_number_bombs=total_number_bombs # we have a limited number of bombs to kill the ghost 
#        Bomb.Remaining_bombs += 1 # to know how many objects that we have built so far         
               
    def is_exploded():
       pass   
#    def update(self,delta):
#        if self.bomberman.demand_release_bomb==False:
#            self.x=self.bomberman.x
#            self.y=self.bomberman.y
#        else:
#            self.released=True
#            self.bomberman.demand_release_bomb= False 
#            
#
class Explosion:
     def __init__(self,maze,world,bomb):
         self.x=bomb.x
         self.y=bomb.y
         self.block_size=bomb.bomberman.block_size
         self.maze=maze
         self.world=world
         self.destroyed_ground_list=[]
     def get_row(self):
        return (self.y - self.block_size) // self.block_size
     def get_col(self):
        return self.x // self.block_size
     def get_explosion_area(self):
        for i in range(-3,2):
            for j in range(-3,2):
                if (self.y+j*self.block_size-self.block_size)//self.block_size<self.maze.height and (self.x+i*self.block_size)//self.block_size<self.maze.width:  
                    if not self.maze.has_wall_at((self.y+j*self.block_size-self.block_size)//self.block_size,(self.x+i*self.block_size)//self.block_size):
                        self.destroyed_ground_list.append(Destroyed_ground(self,self.x+i*self.block_size,self.y+j*self.block_size))
#                    self.destroyed_ground_list.append(Destroyed_ground(self,(self.get_col()+i)*self.block_size,(self.get_row()+j)*self.block_size)) 
        return(self.destroyed_ground_list)            
class Destroyed_ground:
    def __init__(self,explosion,x,y):
        self.explosion=explosion
        self.x=x
        self.y=y
class Ghost:
    def __init__(self, maze, world,block_size):
        self.block_size=block_size
        self.maze=maze
        self.world=world
        self.y=randint(0,self.world.height-60)
        self.x=randint(0,self.world.width-60)
        while self.maze.has_wall_at((self.y - self.block_size) // self.block_size,self.x // self.block_size):
            self.x=randint(0,self.world.width-60)
            self.y=randint(0,self.world.height-60)
        
        
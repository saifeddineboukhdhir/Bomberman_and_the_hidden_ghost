# -*- coding: utf-8 -*-
import arcade
from models import World, Bomberman,Explosion,Ghost 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
class MazeDrawer():
    def __init__(self, maze):
        self.maze = maze
        self.width = self.maze.width
        self.height = self.maze.height
        self.destroyed_ground_spirte_all_bombs=[]
        self.wall_sprite = arcade.Sprite('images/wall.jpg')
        self.destryed_ground_sprite=arcade.Sprite('images/ground.jpg')
        self.bomb_sprite=arcade.Sprite("images/bomb.png")
        self.explosion_sprite=None 
        self.destroyed_ground_sprite=arcade.Sprite('images/ground.jpg')
        self.green_ground_sprite=arcade.Sprite('images/green_ground.jpg')        
#        r,c=randint(1,self.height-1),randint(1,self.width-1)
#        while self.maze.has_wall_at(r,c):
#            r,c=randint(1,self.height-1),randint(1,self.width-1)  
#        self.maze.ghost_coordinate=(r,c)            
    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()   
    def get_sprite_position(self, r, c):
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
        return x,y
    def ghost_is_near(self,r,c):
        for i in range(-3,4 ):
            for j in range(-3,4):
                if self.maze.ghost_coordinate==(r+i,c+j):
                    return(True)
        return(False)             
    def draw(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.maze.has_wall_at(r,c):
                    self.draw_sprite(self.wall_sprite, r, c)
                if self.maze.map[r][c]=="+":
                    self.draw_sprite(self.bomb_sprite,r,c)
                if  self.maze.map[r][c]=="@":
                    self.draw_sprite(self.green_ground_sprite,r,c)
                if self.maze.map[r][c]=="*": 
                    self.draw_sprite(self.destryed_ground_sprite,r,c)
#                    if self.maze.no_bombs and self.maze.demand_explose_bombs==True:
#                        self.maze.game_over=True
                    if (r,c)==self.maze.ghost_coordinate:
                        self.maze.player_wins=True
                        
                    
        if self.maze.demand_explose_bombs:
            self.maze.demand_explose_bombs=False
            for r in range(self.height):
                for c in range(self.width):
                    if self.maze.map[r][c]=="+":
                        self.explosion_sprite=ModelSprite("images/explosion.png",model= Explosion(r,c,BLOCK_SIZE))
                        self.explosion_sprite.draw()
                        for i in range(-1,2):
                            for j in range(-1,2):
                                 if c+j<self.maze.width and r+i<self.maze.height and c+j>0 and r+i>0:
                                     if not self.maze.has_wall_at(r+i,c+j):
                                         if self.ghost_is_near(r+i,c+j):
                                             self.maze.map[r+i]=self.maze.map[r+i][:c+j]+"*"+self.maze.map[r+i][c+j+1:]
                                         else:
                                             self.maze.map[r+i]=self.maze.map[r+i][:c+j]+"@"+self.maze.map[r+i][c+j+1:] 
                                         if self.maze.no_bombs:
                                             self.maze.game_over=True

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()
 
class MazeWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.AERO_BLUE)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)
        self.bomberman_sprite = ModelSprite('images/bomberman.png',
                                         model=self.world.bomberman)
        self.maze_drawer = MazeDrawer(self.world.maze)
#        self.ghost_spirte=ModelSprite('images/ghost.png',model=self.world.ghost)
        
        self.ghost=ModelSprite('images/ghost.png',model= Ghost(self.world.maze.ghost_coordinate[0],self.world.maze.ghost_coordinate[1],BLOCK_SIZE))
    def update(self, delta):
        self.world.update(delta) 
    def on_draw(self):
        arcade.start_render()
        self.maze_drawer.draw()
        self.bomberman_sprite.draw()
#        self.ghost_spirte.draw()
        if self.world.maze.game_over:
            self.world.maze.player_wins=False
            self.ghost.draw()
            arcade.draw_text("You lost",
                          100, self.height - 30,
                         arcade.color.RED, 20)
        if self.world.maze.player_wins:
            self.world.maze.game_over=False
            self.ghost.draw()
            arcade.draw_text("You won",
                          100, self.height - 30,
                         arcade.color.RED, 20)
        arcade.draw_text("Bombs "+str(self.world.bomberman.remaining_bombs),
                         self.width - 110, self.height - 30,
                         arcade.color.RED, 20)

    def on_key_press(self, key, key_modifiers):
         self.world.on_key_press(key, key_modifiers)    
 
 
def main():
    window = MazeWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()

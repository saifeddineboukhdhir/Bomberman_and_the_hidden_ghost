# -*- coding: utf-8 -*-
import arcade
from models import World, Bomberman
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
    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()   
    def get_sprite_position(self, r, c):
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2);
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2));
        return x,y
 
    def draw(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.maze.has_wall_at(r,c):
                    self.draw_sprite(self.wall_sprite, r, c)
        if len(self.maze.destroyed_ground) !=0:
            self.destroyed_ground_spirte_all_bombs=self.destroyed_ground_spirte_all_bombs+self.maze.destroyed_ground
            for destroyed_ground_spirte in self.destroyed_ground_spirte_all_bombs:
                destroyed_ground_spirte.draw()

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
        self.ghost_spirte=ModelSprite('images/ghost.png',model=self.world.ghost)
        
    def update(self, delta):
        self.world.update(delta) 
    def on_draw(self):
        arcade.start_render()
        self.maze_drawer.draw()
        self.bomberman_sprite.draw()
        self.ghost_spirte.draw()
        self.explosion_sprite=[]
        self.explosion_liste=[]
        self.destroyed_ground_list=[]
        self.explosion_area_sprite=[]
        self.draw_destroyed_ground=None

        for i in range( len(self.world.bomberman.bomb_realesed)):
            self.bomb_sprite=ModelSprite('images/bomb.png',
                                         model=self.world.bomberman.bomb_realesed[i])
            self.explosion_liste.append(self.world.bomberman.bomb_realesed[i].explosion)
            self.explosion_sprite.append(ModelSprite('images/explosion.png',model=self.world.bomberman.bomb_realesed[i].explosion))
            self.bomb_sprite.draw()
        if self.world.bomberman.demand_explose_bombs:
            for explosion_sprite in self.explosion_sprite:
                explosion_sprite.draw()
                self.destroyed_ground_list=self.explosion_liste[self.explosion_sprite.index(explosion_sprite)].get_explosion_area()
                self.explosion_area_sprite=[ModelSprite('images/ground.jpg',model=destroyed_ground) for destroyed_ground in self.destroyed_ground_list]
                self.world.maze.destroyed_ground=self.world.maze.destroyed_ground+self.explosion_area_sprite
                self.world.bomberman.bomb_realesed=[]
                self.world.bomberman.demand_explose_bombs=False
                self.draw_destroyed_ground=True 
    def on_key_press(self, key, key_modifiers):
         self.world.on_key_press(key, key_modifiers)    
 
 
def main():
    window = MazeWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()

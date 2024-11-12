from uib_inf100_graphics.helpers.image import load_image, scaled_image, image_in_box
import os
from PIL import ImageOps


class GameObject:
    '''
    Game object class.
    '''
    def __init__(self, engine_reference,  position=[150,150], size=(50,50), hp=100, colliding=True):
        self.size = size
        self.hp = hp
        self.position = position
        self.velocity = [0,0]
        self._engine_reference = engine_reference
        self.colliding=colliding

    ###
    # HANDLE GAME TICK UPDATES.
    ###
    def draw(self, canvas):
        pass


    def game_tick(self):
        #New position.
        self.position[0]+=self.velocity[0]/(self._engine_reference.FPS)
        self.position[1]+=self.velocity[1]/(self._engine_reference.FPS)
        #Handle any collision that might have occured due to new position.
        self.handle_collisions()
        #If health is depleted the object gets deleted.
        if self.hp<=0:
            self.delete()

    def handle_collisions(self):
        #Get all collidable entities.
        for entity in (filter(lambda x: x.colliding, self._engine_reference.states[self._engine_reference.cur_state_index].entities)):
            #No self collision.
            if entity==self:
                continue
            
            #Check for overlap with entity.
            x_overlap = abs(self.position[0] - entity.position[0]) < (self.size[0] / 2.0 + entity.size[0] / 2.0)
            x_border = not (self.size[0]/2 < self.position[0] < self._engine_reference.START_WIDTH-self.size[0]/2) 
            y_overlap = abs(self.position[1] - entity.position[1]) < (self.size[1] / 2.0 + entity.size[1] / 2.0)
            y_border = not (self.size[1]/2 < self.position[1] < self._engine_reference.START_HEIGHT-self.size[1]/2) 
            #Go back one.
            if (x_overlap and y_overlap) or x_border or y_border:
                self.position[0] -= self.velocity[0] * self._engine_reference.timer_delay / 1000 * 1.01
                self.position[1] -= self.velocity[1] * self._engine_reference.timer_delay / 1000 * 1.01
                self.velocity[0]=0
                self.velocity[1]=0

    ###
    # HANDLE USER INTERACTION.
    ##
    def key_pressed(self,key:str):
        pass

    def key_released(self,key:str):
        pass

    def mouse_pressed(self,x:int,y:int):
        pass

    def mouse_released(self,x:int,y:int):
        pass

    ###
    # UTILITIES.
    ###
    def coordinate_in_obj(self,x:int,y:int):
        if (self.position[0]-self.size[0]/2<=x<=self.position[0]+self.size[0]/2)  \
        and (self.position[1]-self.size[1]/2<=y<=self.position[1]+self.size[1]/2):
            return True
        return False

    ###
    # DELETE SELF.
    ##
    def delete(self):
        self._engine_reference.states[self._engine_reference.cur_state_index].entities.remove(self)



class TexturedGameObject(GameObject):
    '''
        Game object class with a loaded image texture.
    '''
    def __init__(self, engine_reference, position=[150,150], size=(50,50), hp=100, texture="media/textures/placeholder.png"):
        super().__init__(engine_reference,position,size,hp)
        self.texture = load_image(texture)
        self.image_direction=True # Right is true, left is false.


    ###
    # HANDLE GAME TICK UPDATES.
    ###
    def draw(self, canvas):
        # Get current frame based on direction
        direction = 'right' if self.image_direction else 'left'
        texture = self.texture if direction == 'right' else ImageOps.mirror(self.texture)

        # Get corners of image
        top_left_x = self.position[0] - self.size[0] / 2
        top_left_y = self.position[1] - self.size[1] / 2
        bottom_right_x = self.position[0] + self.size[0] / 2
        bottom_right_y = self.position[1] + self.size[1] / 2

        # Draw image to canvas
        image_in_box(canvas, top_left_x, top_left_y, bottom_right_x, bottom_right_y, texture, fit_mode="stretch")


class AnimatedGameObject(GameObject):
    '''
        Game object class with animations.
    '''
    def __init__(self, engine_reference, position=[150,150], size=(50,50), hp=100, FPS=16):
        super().__init__(engine_reference,position,size,hp)
        self.animations = {}
        self.cur_animation = ""
        self.cur_frame_index = 0
        self.time_since_last_frame = 0
        self.FPS = FPS
        self.image_direction = True # True is right, left is False.

    def load_animation(self, directory, animation_name):
        # Get all files in directory and sort them alphabetically
        files = sorted(f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')))

        # Load files into textures and create flipped versions
        textures_right = [load_image(os.path.join(directory, file)) for file in files]
        textures_left = [ImageOps.mirror(texture) for texture in textures_right]

        # Add entries into animations dict
        self.animations[animation_name] = {'right': textures_right, 'left': textures_left}

    def change_animation(self, animation):
        self.cur_animation = animation
        self.cur_frame_index = 0
        self.time_since_last_frame = 0

    ###
    # HANDLE GAME TICK UPDATES.
    ###
    def draw(self, canvas):
        # Get current frame based on direction
        direction = 'right' if self.image_direction else 'left'
        texture = self.animations[self.cur_animation][direction][self.cur_frame_index%len(self.animations[self.cur_animation][direction])]

        # Get corners of image
        top_left_x = self.position[0] - self.size[0] / 2
        top_left_y = self.position[1] - self.size[1] / 2
        bottom_right_x = self.position[0] + self.size[0] / 2
        bottom_right_y = self.position[1] + self.size[1] / 2

        # Draw image to canvas
        image_in_box(canvas, top_left_x, top_left_y, bottom_right_x, bottom_right_y, texture, fit_mode="stretch")

        # Update animation information
        if self.time_since_last_frame >= (1000 / self.FPS):
            self.cur_frame_index += 1
            self.cur_frame_index %= len(self.animations[self.cur_animation][direction])
            self.time_since_last_frame = 0
        self.time_since_last_frame += self._engine_reference.timer_delay
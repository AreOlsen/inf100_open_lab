from engine import State
from scripts.game_obj import TexturedGameObject
from scripts.game import Game
import os

class Board(TexturedGameObject):
    def __init__(self,  engine_reference, position=[150,150], size=(220,100), texture="media/textures/hud/banner.png",text=""):
        super().__init__(engine_reference,position,size,float("inf"),texture)
        self.text=text

    def draw(self,canvas):
        super().draw(canvas)
        canvas.create_text(self.position[0], self.position[1], text=self.text,
                        font="Arial 20 bold", fill="white")


class RedirectButton(TexturedGameObject):
    def __init__(self,  engine_reference, position=[150,150], size=(220,100), texture="media/textures/hud/banner.png", redirect_state_index = 1, text=""):
        super().__init__(engine_reference,position,size,float("inf"),texture)
        self.redirect_state_index=redirect_state_index
        self.text=text

    def draw(self,canvas):
        super().draw(canvas)
        canvas.create_text(self.position[0], self.position[1], text=self.text,
                        font="Arial 20 bold", fill="black")


    def mouse_pressed(self,x,y):
        if self.coordinate_in_obj(x,y):
            self._engine_reference.cur_state_index=self.redirect_state_index

class NewGameButton(RedirectButton):
    def __init__(self,  engine_reference, position=[150,150], size=(220,100), texture="media/textures/hud/banner.png", redirect_state_index = 1, text=""):
        super().__init__(engine_reference,position,size,texture,redirect_state_index,text)

    def mouse_pressed(self,x,y):
        if self.coordinate_in_obj(x,y):
            self._engine_reference.states[1]=Game(self._engine_reference)
            self._engine_reference.cur_state_index=self.redirect_state_index


class LoadGameButton(RedirectButton):
    def __init__(self,  engine_reference, position=[150,150], size=(220,100), texture="media/textures/hud/banner.png", redirect_state_index = 1,text=""):
        super().__init__(engine_reference,position,size,texture,redirect_state_index,text)

    def mouse_pressed(self,x,y):
        if self.coordinate_in_obj(x,y):
            self._engine_reference.states[1]=Game()
            self._engine_reference.states[1].load_game(game_save_path="save/save.json")
            self._engine_reference.cur_state_index=self.redirect_state_index




class Menu(State):
    def __init__(self, background_texture, menu_elements=[]):
        super().__init__(menu_elements, background_texture)

class StartMenu(Menu):
    '''
    Predefined start menu with a start button,
    (if a save is stored) load save button, 
    instructions button.
    '''

    def __init__(self, engine_reference, background_texture="media/textures/backdrops/menu.png", button_texture="media/textures/hud/banner.png"):
        super().__init__(background_texture=background_texture)
        self.entities=[]
        self.engine_reference=engine_reference
        self.button_texture = button_texture

        #New game.
        self.entities.append(
            NewGameButton(engine_reference=engine_reference,texture=button_texture,redirect_state_index=1,text="New game.")
        )

        #Load game.
        if os.path.exists("save/save.json"):
            self.entities.append(
                LoadGameButton(engine_reference=engine_reference,texture=button_texture,redirect_state_index=1, text="Load game.")
            )

        #Instructions.
        self.entities.append(
            RedirectButton(engine_reference=engine_reference, texture=button_texture,redirect_state_index=3, text="Instructions")
        )

        #Position all buttons evenly.
        for button_i, button in enumerate(self.entities):
            button.position[0]=button._engine_reference.width/2
            button.position[1]=(button_i+1)*(button._engine_reference.height/(len(self.entities)+1))


class GameOverMenu(Menu):
    def __init__(self, engine_reference, background_texture, button_texture, text=""):
        #Initialize backdrop & board.
        super().__init__(menu_elements=[
            Board(engine_reference,
            [engine_reference.width/2,
            engine_reference.height/2]
            ,size=(engine_reference.width/2,
            engine_reference.height/1.5),
            texture="media/textures/hud/board.png",text=text)],
            background_texture=background_texture)
        
        #Add redirect button to main menu.
        self.entities.append(
            RedirectButton(
                engine_reference=engine_reference,
                position=[engine_reference.width/2,
                engine_reference.height*2/3],
                texture=button_texture,
                redirect_state_index=0,
                text="Main menu.")
        )

class Instructions(State):
    def __init__(self, engine_reference, background_texture, instructions=""):
        super().__init__(entities=[Board(engine_reference,[engine_reference.width/2,engine_reference.height/2],size=(engine_reference.width/2,engine_reference.height/1.5), texture="media/textures/hud/board.png",text=instructions)],background_texture=background_texture)

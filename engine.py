from uib_inf100_graphics.event_app.uib_inf100_graphics import App 
from uib_inf100_graphics.helpers.image import load_image, image_in_box

class State:
    '''
    Simple state system.
    (uibinf100graphics has similar, but is more tedious and unscalable.)
    '''
    def __init__(self, engine_reference, entities=[], background_texture="media/textures/placeholder.png"):
        self.entities = entities
        self._engine_reference = engine_reference
        self.background_texture = background_texture
        self.background = None
        if background_texture != "":
            self.background = load_image(background_texture)

    def game_tick(self):
        pass

    def draw(self, canvas):
        #Draw background.
        if self.background != None:
            image_in_box(canvas,0,0,self._engine_reference.width,self._engine_reference.height,self.background,fit_mode="stretch")


class Engine(App):
    '''
    Simple wrapper for uib inf100 app class.
    '''
    def __init__(self, states=[], width=1280, height=720, FPS=100, title="Monster Survival."):
        # All states.
        # Normally state 0 is the menu.
        self.states = states
        self.cur_state_index = 0
        self.START_WIDTH = width
        self.START_HEIGHT = height
        self.FPS = FPS

        #Default init.
        super().__init__(width=width,height=height,title=title, autorun=False)


        # Set FPS.
        self.timer_delay = int(1000/FPS) #Ms.


    ###
    # FRAME UPDATE.
    ###
    def timer_fired(self):
        #State gametick.
        self.states[self.cur_state_index].game_tick()

        #Entity gametick.
        for entity in self.states[self.cur_state_index].entities:
            entity.game_tick()

    def redraw_all(self,canvas): 
        #Draw state related things, such as background.
        self.states[self.cur_state_index].draw(canvas)

        #Draw entities.
        for entity in self.states[self.cur_state_index].entities:
            entity.draw(canvas)



    ###
    # INPUT HANDLING.
    # Transfer input handling to each object for organization.
    ###
    def key_released(self,event):
        #Entity key handling.
        for entity in self.states[self.cur_state_index].entities:
            #Entities handle key presses differently.
            entity.key_released(key=event.key)

    def key_pressed(self, event):
        if event.key=="Escape":
            #If in game.
            if self.cur_state_index==1:
                #Save game data.
                self.states[1].save_game()

            #Go back to main menu.
            self.cur_state_index=0

            #Refresh start menu.            
            self.states[0].__init__(self)

        #Entity key handling.
        for entity in self.states[self.cur_state_index].entities:
            #Entities handle key presses differently.
            entity.key_pressed(key=event.key)


    def mouse_pressed(self, event):
        #Entity 
        for entity in self.states[self.cur_state_index].entities:
            #Entities handle mouse presses differntly.
            x, y = event.x, event.y
            entity.mouse_pressed(x,y)

    def mouse_released(self, event):
        #Entity 
        for entity in self.states[self.cur_state_index].entities:
            #Entities handle mouse presses differntly.
            x, y = event.x, event.y
            entity.mouse_released(x,y)


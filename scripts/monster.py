from scripts.game_obj import TexturedGameObject


class Monster(TexturedGameObject):
    def __init__(self,engine_reference, size=(100,100)):
        super().__init__(engine_reference,size=size, texture="media/textures/monster/monster.png")
        self.SPEED = 5000

    def game_tick(self):
        super().game_tick()
        player = self._engine_reference.states[self._engine_reference.cur_state_index].entities[0]
        #Point monster towards player.
        self.velocity[0]=self.position[0]-player.position[0]
        self.velocity[1]=self.position[1]-player.position[1]
        #Scale velocity vectors to have correct SPEED.
        velocity_length = (self.velocity[0]**2+self.velocity[1]**2)**0.5
        self.velocity[0]*=(self.SPEED)/velocity_length
        self.velocity[1]*=(self.SPEED)/velocity_length

    def draw(self,canvas):
        super().draw(canvas)
        #Print monster hp.
        canvas.create_text(self.position[0], self.position[1]-80, text=f"HP: {self.hp}", font="Arial 20 bold", fill="red")




    def mouse_pressed(self, x,y):
        if self.coordinate_in_obj(x,y):
            print("Pressed")
            player = self._engine_reference.states[self._engine_reference.cur_state_index].entities[0]
            player.attack(self)
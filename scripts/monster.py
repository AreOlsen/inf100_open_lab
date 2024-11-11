from scripts.game_obj import TexturedGameObject
import time

class Monster(TexturedGameObject):
    def __init__(self,engine_reference, size=(100,100)):
        super().__init__(engine_reference,size=size, texture="media/textures/monster/monster.png")
        self.SPEED = 50

        self.player_reference = self._engine_reference.states[self._engine_reference.cur_state_index].entities[0]

        self.ATTACK_RANGE = max(self.player_reference.size[0],self.player_reference.size[1])+max(self.size[0],self.size[1])
        self.ATTACK_DAMAGE = 20
        self.ATTACK_COOLDOWN_SECS = 2
        self.last_attack_epoch = time.time_ns()


    def game_tick(self):
        super().game_tick()
        player=self.player_reference
        #Check if in attack range -> attack -> skip walking towards player.
        distance_monster_player = ((self.position[0]-player.position[0])**2+(self.position[1]-player.position[1])**2)**0.5
        if distance_monster_player<=self.ATTACK_RANGE:
            if (time.time_ns()-self.last_attack_epoch)>=self.ATTACK_COOLDOWN_SECS*10**9:
                player.hp-=self.ATTACK_DAMAGE
                self.last_attack_epoch=time.time_ns()
            return

        #Point monster towards player.
        self.velocity[0]=player.position[0]-self.position[0]
        self.velocity[1]=player.position[1]-self.position[1]

        #Decide direction of texture.
        self.image_direction=False
        if self.velocity[0]>=0:
            self.image_direction=True


        #Scale velocity vectors to have correct SPEED.
        velocity_length = (self.velocity[0]**2+self.velocity[1]**2)**0.5
        if velocity_length!=0:
            self.velocity[0]*=(self.SPEED)/(velocity_length)
            self.velocity[1]*=(self.SPEED)/(velocity_length)

    def draw(self,canvas):
        super().draw(canvas)
        #Print monster hp.
        canvas.create_text(self.position[0], self.position[1]-80, text=f"HP: {self.hp}", font="Arial 20 bold", fill="red")

    def mouse_pressed(self, x,y):
        if self.coordinate_in_obj(x,y):
            player = self._engine_reference.states[self._engine_reference.cur_state_index].entities[0]
            player.attack(self)
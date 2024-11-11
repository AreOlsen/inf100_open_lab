from scripts.game_obj import TexturedGameObject, AnimatedGameObject
import os 
import time

class Player(AnimatedGameObject):
    def __init__(self,engine_reference, size=(100,100)):
        super().__init__(engine_reference,size=size)
        self.load_animation("media/textures/soldier_idle", "idle")
        self.cur_animation="idle"
        self.SPEED = 1000
        self.ATTACK_DAMAGE = 25
        self.ATTACK_RANGE = 1000
        self.ATTACK_COOLDOWN_SECS = 1
        self.last_attack_epoch = time.time_ns()

    def draw(self,canvas):
        super().draw(canvas)
        #Create text of hp.
        canvas.create_text(self.position[0], self.position[1]-80, text=f"HP: {self.hp}", font="Arial 20 bold", fill="black")


    def delete(self):
        super().delete()
        #Change to game over screen.
        self._engine_reference.cur_state_index=2
        #Delete if there is a current save for current game.
        if os.path.exists("save/save.json"):
            os.remove("save/save.json")
            self._engine_reference.states[1].__init__(self._engine_reference)

    def key_released(self,key):
        match key:
            case "w" | "s":
                self.velocity[1]=0
            case "a" | "d":
                self.velocity[0]=0

    def key_pressed(self,key):
        #Change directions.
        match key:
            case "w":
                self.velocity[1]=-self.SPEED
            case "s":
                self.velocity[1]=self.SPEED
            case "d":
                self.velocity[0]=self.SPEED
                self.image_direction=True
            case "a":
                self.velocity[0]=-self.SPEED
                self.image_direction=False
    
    def attack(self, monster):
        #If still in cooldown.
        if (time.time_ns()-self.last_attack_epoch)<self.ATTACK_COOLDOWN_SECS*10**9:
            return

        #If monster out of range.
        distance_monster_player = ((self.position[0]-monster.position[0])**2+(self.position[1]+monster.position[1])**2)**0.5
        if distance_monster_player>=self.ATTACK_RANGE:
            return

        #Attack monster.
        monster.hp -= self.ATTACK_DAMAGE
        print(monster.hp)
        self.last_attack_epoch=time.time_ns()
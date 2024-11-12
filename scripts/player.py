from scripts.game_obj import TexturedGameObject, AnimatedGameObject
import os 
import time

class Player(AnimatedGameObject):
    def __init__(self,engine_reference, size=(100,100)):
        super().__init__(engine_reference,size=size)
        self.load_animation("media/textures/soldier/idle", "idle")
        self.load_animation("media/textures/soldier/walk", "walk")
        self.load_animation("media/textures/soldier/attack", "attack")
        self.cur_animation="idle"
        self.SPEED = 1000
        self.ATTACK_DAMAGE = 25
        self.ATTACK_RANGE = 1000
        self.ATTACK_COOLDOWN_SECS = len(os.listdir("media/textures/soldier/attack"))/self.FPS #GET SECONDS OF ATTACK ANIMATION.
        self.last_attack_epoch = time.time()
        self.IN_ATTACK = False

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
                self.cur_animation="idle"
            case "a" | "d":
                self.velocity[0]=0
                self.cur_animation="idle"

    def key_pressed(self,key):
        if self.IN_ATTACK:
            return
        
        #Change directions.
        match key:
            case "w":
                self.velocity[1]=-self.SPEED
                if self.cur_animation!="attack":
                    self.cur_animation="walk"
            case "s":
                self.velocity[1]=self.SPEED
                if self.cur_animation!="attack":
                    self.cur_animation="walk"
            case "d":
                self.velocity[0]=self.SPEED
                self.image_direction=True
                if self.cur_animation!="attack":
                    self.cur_animation="walk"
            case "a":
                self.velocity[0]=-self.SPEED
                self.image_direction=False
                if self.cur_animation!="attack":
                    self.cur_animation="walk"
    
    def attack(self, monster):
        self.IN_ATTACK=False

        #If still in cooldown.
        if (time.time() - self.last_attack_epoch)<self.ATTACK_COOLDOWN_SECS:
            self.IN_ATTACK=True
            return
        
        self.cur_animation="attack"

        self.last_attack_epoch=time.time()

        #If monster out of range.
        distance_monster_player = ((self.position[0]-monster.position[0])**2+(self.position[1]+monster.position[1])**2)**0.5
        if distance_monster_player<=self.ATTACK_RANGE:
            monster.hp -= self.ATTACK_DAMAGE
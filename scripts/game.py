from engine import State
from scripts.player import Player
from scripts.monster import Monster
import json
import random

class Game(State):
    def __init__(self, engine_reference, background_texture="media/textures/backdrops/game.png"):
        super().__init__(entities=[Player(engine_reference=engine_reference)],background_texture=background_texture)
        self.round = 0
        self.MAX_MONSTERS = 10
        self._engine_reference=engine_reference


    def spawn_monster(self, tries_to_spawn=10):
        monster = Monster(self._engine_reference)
        for _ in range(tries_to_spawn):  # Try to spawn a monster up to n times. 
            #Random position.
            pos_x = random.randrange(start=0,stop=int(self._engine_reference.START_WIDTH-monster.size[0]/2*1.2),step=1)
            pos_y = random.randrange(start=0,stop=int(self._engine_reference.START_HEIGHT-monster.size[1]/2*1.2),step=1)

            #Check if the current random position is in collision with another object.
            collision_detected = False
            for entity in self.entities:
                # Check all the corners of the monster to see if colliding with any object.
                corners = [
                    (pos_x - monster.size[0] / 2, pos_y - monster.size[1] / 2),
                    (pos_x + monster.size[0] / 2, pos_y - monster.size[1] / 2),
                    (pos_x - monster.size[0] / 2, pos_y + monster.size[1] / 2),
                    (pos_x + monster.size[0] / 2, pos_y + monster.size[1] / 2)
                ]
                #Inside another entity.
                for corner in corners:
                    if entity.coordinate_in_obj(corner[0], corner[1]):
                        collision_detected = True
                        break
                #Break out of entities checking loop.
                if collision_detected:
                    break

            #Next random position iteration.
            if collision_detected:
                continue

            #If not in any already spawned entities -> spawn the monster.
            monster.position[0]=pos_x
            monster.position[1]=pos_y
            self.entities.append(monster)
            break


    def spawn_monsters(self):
        for i in range(min(self.MAX_MONSTERS,self.round*2+1)):
            self.spawn_monster()


    def new_round(self):
        self.round+=1
        print(self.round)
        self.spawn_monsters()


    def game_tick(self):
        #If only player alive.
        if len(self.entities)==1:
            self.new_round()

    def load_game(self,game_save_path):
        json_data = json.load("save/save.json")
        for entity_index, entity in enumerate(json_data["entities"]):
            if entity_index<len(self.entities):
                self.entities[entity_index].position = [entity["pos_x"], entity["pos_y"]]
                self.entities[entity_index].hp = entity["hp"]
            elif entity["game_object_type"]=="monster":
                self.entities.append(Monster(self._engine_reference))
            elif entity["game_object_type"]=="player":
                self.entities.append(Player(self._engine_reference))
            else:
                print("Unknown entity type.")

    def save_game(self):
        try:
            data = {}
            data["entities"]=[]
            for entity in self.entities:
                data["entities"].append({
                    "game_object_type":entity.__class__.__name__.lower(),
                    "hp":entity.hp,
                    "pos_x":entity.position[0],
                    "pos_y":entity.position[1]
                })
            self.entities=[]
            with open("save/save.json", "w") as outfile:
                json.dump(data, outfile)
        except Exception:
            print("Not possible to save game save.")


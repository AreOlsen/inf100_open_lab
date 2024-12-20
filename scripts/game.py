from engine import State
from scripts.player import Player
from scripts.monster import Monster
import json
import random

class Game(State):
    def __init__(self, engine_reference, background_texture="media/textures/backdrops/game.png"):
        super().__init__( engine_reference,entities=[Player(engine_reference=engine_reference)],background_texture=background_texture)
        self.round = 0
        self.MAX_MONSTERS = 10
        self._engine_reference=engine_reference

    def spawn_monster(self, tries_to_spawn = 10,monster_size = (150,150)):
        """
            We try to spawn a monster n times, if we can't place one, we give up might be no available positions. 
        """

        for _ in range(tries_to_spawn):
            available_spawn_position = True

            pos_x = random.random()*(self._engine_reference.START_WIDTH - monster_size[0]/2)
            pos_y = random.random()*(self._engine_reference.START_HEIGHT - monster_size[1]/2)

            monster_corners = [
                (pos_x - monster_size[0] / 2, pos_y - monster_size[1] / 2),
                (pos_x + monster_size[0] / 2, pos_y - monster_size[1] / 2),
                (pos_x - monster_size[0] / 2, pos_y + monster_size[1] / 2),
                (pos_x + monster_size[0] / 2, pos_y + monster_size[1] / 2)
            ]

            #Check if collision with any monster.
            for entity in self.entities:
                #To check for collisions, we check the corners.
                for corner in monster_corners:
                    if entity.coordinate_in_obj(corner[0],corner[1]):
                        available_spawn_position=False
            
            # Check if the monster is for some reason within the screen borders
            for corner in monster_corners:
                if corner[0] < 0 or corner[0] > self._engine_reference.START_WIDTH or corner[1] < 0 or corner[1] > self._engine_reference.START_HEIGHT:
                    available_spawn_position = False
                    break

            if available_spawn_position:
                monster = Monster(self._engine_reference,monster_size)
                monster.position = [pos_x,pos_y]
                self.entities.append(monster)
                break


    def spawn_monsters(self):
        print("Ran spawn monsters")
        for i in range(min(self.MAX_MONSTERS,self.round*2-1)):
            self.spawn_monster()


    def new_round(self):
        self.round+=1
        print(f"Current round : {self.round}")
        self.spawn_monsters()


    def game_tick(self):
        #If only player alive.
        if len(self.entities)==1:
            self.new_round()

    def draw(self, canvas):
        super().draw(canvas)

        #Draw current round information.
        canvas.create_text(150, 30, text=f"Current round: {self.round}", font="Arial 20 bold", fill="black")



    def load_game(self,game_save_path="save/save.json"):
        with open(game_save_path, "r+") as file:
            json_data = json.load(file)
            self.round = json_data["round"]
            for entity_index, entity in enumerate(json_data["entities"]):
                if entity_index<len(self.entities):
                    self.entities[entity_index].position = [entity["pos_x"], entity["pos_y"]]
                    self.entities[entity_index].hp = entity["hp"]
                    self.entities[entity_index].size = entity["size"]
                elif entity["game_object_type"]=="monster":
                    monster = Monster(self._engine_reference, entity["size"])
                    monster.position = [entity["pos_x"], entity["pos_y"]]
                    monster.hp = entity["hp"]
                    self.entities.append(monster)
                elif entity["game_object_type"]=="player":
                    player = Player(self._engine_reference)
                    player.position = [entity["pos_x"], entity["pos_y"]]
                    player.hp = entity["hp"]
                    player.size = entity["size"]
                    self.entities.append(player)
                else:
                    print("Unknown entity type.")

    def save_game(self, game_save_path="save/save.json"):
        try:
            data = {}
            data["round"]=self.round
            data["entities"]=[]
            for entity in self.entities:
                data["entities"].append({
                    "game_object_type":entity.__class__.__name__.lower(),
                    "hp":entity.hp,
                    "pos_x":entity.position[0],
                    "pos_y":entity.position[1],
                    "size":entity.size
                })
            self.entities=[]
            with open(game_save_path, "w+") as outfile:
                json.dump(data, outfile)
        except Exception as e:
            print("Not possible to save game save.")
            print(f"Error : {e}")


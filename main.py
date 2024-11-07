from engine import Engine
from scripts.game_obj import TexturedGameObject
from scripts.player import Player
from scripts.menu import Menu, RedirectButton, StartMenu, GameOverMenu,Instructions
from scripts.game import Game

'''
STATES:
0. MENU.
1. GAME.
2. GAME OVER.
3. INSTRUCTIONS
'''


game = Engine()
game.states=[
        #Menu.
        StartMenu(engine_reference=game, background_texture="media/textures/backdrops/menu.png",button_texture="media/textures/hud/banner.png"),
        Game(engine_reference=game),
        GameOverMenu(game,background_texture="media/textures/backdrops/menu.png",button_texture="media/textures/hud/banner.png",text="You lost!"),
        Instructions(game,
        background_texture="media/textures/backdrops/menu.png",
        instructions="""
            W - upwards \n
            S - downwards\n
            D - right \n
            A - left \n
            Left click - attack\n
            Esc - menu.
        """
        )
    ]

game.run()

"""Quit the game command."""


def quit_game(game, *args, **kwargs):
    """We are LEAVING!"""
    game.is_running = False

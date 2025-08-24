"""Quit the game command."""


def quit_game(game, *args, **kwargs) -> None:
    """We are LEAVING!"""
    game.is_running = False
    return

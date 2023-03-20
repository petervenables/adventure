# Adventure Game

## Motivation

This is my exploration of developing a game in the spirit of the old text-based adventure games I recall from the early days of computer gaming. I have some recollection of playing a game like this but, at this time, I have done no research into the specific games. I know there may have been a game called "Adventure" even and if I decide to change the name of this game because of that, that will be done later. I was inspired to do this while getting a demo of my kid's school assignment which was an implementation of a text-based room and inventory system. 

## Concepts I want to carry forward

I would like to give the player a growing and developing set of verbs they can perform based on their experiences in the game. For example, they player will initially start in a room that will have one or more exits. They may be inclined to assume the direction "North" is up and type "Go North" or just "Go N" but the game will inform them that they do not know which way North is. Later, they may acquire a compass and be able to use Compass directions as nouns in the command set. 

## Principles

The principles of this game are:

- be fun
- don't be tedious
- reward exploration
- create tension where possible
- punish foolishness

To explain this in more detail...

### Be fun

First and foremost, this is a game. It should be interesting and engaging such that the player looks forward to playing it.

### Don't be tedious

A game like this has tough competition compared to graphical games we all know and love. So we should play to the strengths of the medium and not into the weaknesses. If we can make it easy for the player to know what their options are or simplify the typing experience, we should do that. Shortcuts and autocomplete are something to consider. Making the player execute a long series of actions just to do something simple (i.e. going through a door) should be avoided. 

```
In the case where the player wants to exit a room by a closed door, for example, a tedious solution would be:
> Go through door
You can't pass through the door, it is a solid barrier.
> Open door
The door is locked
> Unlock door
With what? Your bare hands?
> Unlock door with key
You try the key on the door and it unlocks!
> Open door
The door opens 
```

In the example above, it may be better to chain events that are likely such as "you unlocked the door, would you like to also open it? (y/n)" or "the door is locked, would you like to try your key? (y/n)"

### Reward Exploration

The game should be an exploration within the mind's eye of the player. As such, interesting descriptions and hidden objects should be littered through the game to entice the player into exploring and experimenting with the things they encounter. A highly engaged player will even want to map their progress in some cases or take notes of puzzle elements they encounter. 

### Create Tension Where Possible

The game world should be mysterious and even dangerous. The player should be aware that the game could end suddenly if they aren't cautious. Things that are obviously dangerous should be threatening. There might be consequences of questionable choices, like the player is poisoned, crippled, or knocked unconcsious for a short time. 

### Punish Foolishness

If the player is standing near a cliff to the East and the player takes the action "Go East" oblige them. It may be sensible (and in the confines of puzzles) to give the player a confirmation in such cases like "It looks like a long way down, are you sure? (y/n)" but in many cases if the player chooses an obviously lethal action, they should experience the consequences of their choices. They may not always be lethal or game-ending but there should be consequences for silliness. 


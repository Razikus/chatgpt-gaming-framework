# ChatGPT gaming framework


## What's this?

My personal fun research on capabilities of ChatGPT and GPT models for gaming

I strongly believe that we can expect some revolution on Non Playable Characters and overall in gaming industry

## DEMO
https://gptgames.razikus.tech/ - I will keep it until some free credits expires

You can also just run your own instance of this

Fill .env file with 
```
APIKEY=xxx
```
from OpenAI API keys page

and execute 
```
docker compose up -d 
```
Your instance will show up on localhost:80


# Video
[![ChatGPT gaming framework](https://img.youtube.com/vi/SR8MkFWrjEo/0.jpg)](https://www.youtube.com/watch?v=SR8MkFWrjEo)




# Target 0

Make a little Proof of Concept to use ChatGPT in order to create a "framework" for creating a text based games in different worlds.

With filling up some basic parameters framework should be able to generate a Game

# Architecture

![Architecture](https://raw.githubusercontent.com/Razikus/chatgpt-gaming-framework/master/arch.png)

Architecture is very easy - main component is Storyteller which is responsible for starting a story, continuing a conversation and parametrize initial prompt.

Model is responsible for continuin a story based on previous conversation.

Memory is responsible for saving a retrieving conversations.

Currently Storyteller is just a seed for a conversation - it just parametrizes a initial prompt, and game goes unmanaged from that one.

In future versions Storyteller could be more specific - evil / good / random / funny / fluffy.

# Version 0 

Version 0 includes

- [x] Working API
- [x] Working library https://pypi.org/project/chatgpt-gaming-framework/
- [x] Working simple GUI


# Main code insights

- Storyteller https://github.com/Razikus/chatgpt-gaming-framework/blob/master/library/chatgpt_gaming_framework/storyteller/storyteller.py
- Async GPT stream model https://github.com/Razikus/chatgpt-gaming-framework/blob/master/library/chatgpt_gaming_framework/models/chatgptmodel.py
- Memory https://github.com/Razikus/chatgpt-gaming-framework/blob/master/library/chatgpt_gaming_framework/memory/redismemory.py
- Example usage https://github.com/Razikus/chatgpt-gaming-framework/blob/master/gamesapi/src/main.py#L110

# Known limitations
- Game will crash in longer run - ChatGPT supports up to X tokens
- Sometimes choosing 1) 2) or 3) doesn't really trigger an action
- Sometimes

# Future

Stage 1 - multiple dimension world.
- [ ] Possibility to introduce NPCs into the game (Leo, bartendeer, very fat and brave). NPCs should have a summary knowledge from other parts of the world.
- [ ] Ability to switch between NPCs during chat (go to tavern talk to Leo)
- [ ] Events based on conditions (Player asked Leo to go with him, does it happen? Yes -> burn tavern)
- [ ] Make summary of conversation during a game because of current ChatGPT constraints (or change model)
- [ ] Introduce new models or replace ChatGPT with something that can be hosted to overcome the limits
- [ ] Move and test with GPT-4

Stage 2 - inventory and skills
- [ ] Possibility to introduce basic inventory to the game and constraints
- [ ] Basic skills - you have to learn swimming in order to swim

Stage 3 - voice
- [ ] Possibility to generate voice to NPCs
- [ ] Possibility to steer the game with the voice


# License

MIT

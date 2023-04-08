from pydantic import BaseModel
from typing import List
from ..models.chatgptmodel import ChatGPTModel
from ..types.types import Conversation, ConversationList
import uuid
import time

class Rule(BaseModel):
    description: str


ProgressionSlowRule = Rule(description="Progression should be slow, so the player can get to know the world and the characters.")
NotStraightForwardRule = Rule(description="The goal should not be straighforward - not all actions should let into main goal")
UnrelatedAndImpossibleForbidden = Rule(description="Don't allow user to do impossible things and something unrelated to the story.")
DoNotEndStoryRule = Rule(description="Do not end the story")
ShouldNotImmediatelyKnowAboutMainGoal = Rule(description = "Player should not be immediately informed about main goal")

EndingRule = Rule(description="""At the end always type a suggested possible short actions to do in format:
1) description of action 1
2) description of action 2
3) description of action 3
It should also contains only one set of action""")

class World(BaseModel):
    year: str
    shortStory: str
    playerRole: str
    assistantRole: str
    playerShortCharacteristic: List[str]
    mainGoal: str

class StoryTellerOptions(BaseModel):
    rules: List[Rule]
    endingRule: Rule
    world: World


class StoryTeller:
    def __init__(self, model: ChatGPTModel, options: StoryTellerOptions):
        self.model = model
        self.options = options
        self.world = self.options.world
        self.initialPrompt = self.generateInitialPrompt()
        

    def getNewConversationUUID(self):
        return str(int(time.time())) + ":" + str(uuid.uuid4())
    
    async def startANewStory(self, uuidOf: str):
        return self.model.streamStartConversation(uuidOf, Conversation(role = "system", content = self.initialPrompt))
    

    async def continueStory(self, storyID: str, message: str):
        return self.model.streamNextStage(storyID, message, None)
    

    def generateInitialPrompt(self):
        playerCharacteristics = '\n'.join(self.world.playerShortCharacteristic)
        rules = '\n'.join([rule.description for rule in self.options.rules])
        return f"""
You are a {self.world.assistantRole} in the game. 
User is the {self.world.playerRole} in the game. 

Story:
Its {self.world.year} year.
{self.world.shortStory}

Main goal:
{self.world.mainGoal}

Player characteristics:
{playerCharacteristics}

Rules:
{rules}

{self.options.endingRule.description}
"""
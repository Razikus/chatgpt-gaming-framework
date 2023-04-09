from fastapi import FastAPI, Depends, HTTPException, Request
from chatgpt_gaming_framework.memory.redismemory import RedisMemory
from chatgpt_gaming_framework.models.chatgptmodel import ChatGPTModel
from chatgpt_gaming_framework.types.types import Conversation, ConversationList
from chatgpt_gaming_framework.storyteller.storyteller import *
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel
from .ratelimit import luaScript
from fastapi.middleware.cors import CORSMiddleware
import os


class StoryTellerMetadata(BaseModel):
    music: str = None


class StartConversationRequest(BaseModel):
    storyTellerOptions: StoryTellerOptions = None
    metadata: StoryTellerMetadata = StoryTellerMetadata(music = "atlantis.mp3")

class GetStoryTellerOptions(BaseModel):
    id: str

class GetConversation(BaseModel):
    id: str

class ConversationRequest(BaseModel):
    id: str
    content: str
origins = [
    "*",
]


app = FastAPI(docs_url="/storyteller/docs", redoc_url="/storyteller/redoc", title="Storyteller API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

defaultStoryTellers = [
    StoryTellerOptions(
        rules = [ProgressionSlowRule, NotStraightForwardRule, UnrelatedAndImpossibleForbidden, DoNotEndStoryRule, ShouldNotImmediatelyKnowAboutMainGoal],
        endingRule=EndingRule,
        world = World(
            year = "1876",
            shortStory="""The story should be about young boy Jack who wants to be a king of Atlantis.
    The player is a boy who lives still on the earth but sometimes sees an mermaid looking at his boat, but immediately hides.
    Nobody know that, but mermaids are forbidden to talk with humans.""",
            playerRole = "player",
            assistantRole = "narrator",
            playerShortCharacteristic = ["poor fisherman child", "often he is telling some jokes"],
            mainGoal="Become a king of atlantis"
        )
    )
]

redisurl = os.environ.get("REDISURL", "localhost")
apikey = os.environ.get("APIKEY") 


limiterScript = None

async def getRedisMemory():
    return RedisMemory(redisurl=redisurl)

async def getChatGPTModel():
    memory = await getRedisMemory()
    return ChatGPTModel(apikey, memory)

async def getNewStoryTeller(options: StoryTellerOptions):
    model = await getChatGPTModel()
    return StoryTeller(model, options)

async def getStoryTeller(conversationID: str):
    model = await getChatGPTModel()
    retrievedStoryTeller = await model.memory.redis.get("STORYTELLER_OPTIONS:" + conversationID)
    if retrievedStoryTeller is None:
        raise HTTPException(404, "Storyteller not found")
    options = StartConversationRequest.parse_raw(retrievedStoryTeller)
    return StoryTeller(model, options.storyTellerOptions)

@app.on_event("startup")
async def startup():
    global limiterScript
    redisMemory = await getRedisMemory()
    limiterScript = redisMemory.redis.register_script(luaScript)


async def checkForRateLimit(id, perSeconds, maxRequests):
    limiterScriptResult = await limiterScript(keys = [id], args = [perSeconds, maxRequests])
    if limiterScriptResult == 0:
        return True
    else:
        raise HTTPException(429, "Rate limit exceeded")

async def saveMetadataForConversation(id, redisClient, metadata):
    await redisClient.set("STORYTELLER_OPTIONS:" + id, metadata.json())


@app.post("/storyteller/start")
async def startConversation(req: StartConversationRequest, rawRequest: Request):
    await checkForRateLimit("RT:" + rawRequest.client.host, 60, 399) 
    if req.storyTellerOptions is None:
        req.storyTellerOptions = defaultStoryTellers[0]
    model = await getNewStoryTeller(req.storyTellerOptions)
    newConversationUUID = model.getNewConversationUUID()
    await saveMetadataForConversation(newConversationUUID, model.model.memory.redis, req)
    async def iterit():
        async for item in await model.startANewStory(newConversationUUID):
            yield json.dumps(item) + "\n"
    return StreamingResponse(iterit(), media_type="application/json")



@app.post("/storyteller/continue")
async def continueConversation(req: ConversationRequest, rawRequest: Request):
    await checkForRateLimit("RT:" + rawRequest.client.host, 60, 3099)
    await checkForRateLimit("RT:" + req.id, 60, 3990)
    model = await getStoryTeller(req.id)
    async def iterit():
        async for item in await model.continueStory(req.id, req.content):
            yield json.dumps(item) + "\n"
    return StreamingResponse(iterit(), media_type="application/json")

@app.post("/storyteller/getForConversation")
async def getStoryTellerForConversation(req: GetStoryTellerOptions, rawRequest: Request):
    await checkForRateLimit("RT:" + rawRequest.client.host, 60, 309)
    await checkForRateLimit("RT:" + req.id, 60, 3099)
    model = await getStoryTeller(req.id)
    meta = await model.model.memory.redis.get("STORYTELLER_OPTIONS:" + req.id)
    return StartConversationRequest.parse_raw(meta)

@app.post("/storyteller/getConversation")
async def getConversation(req: GetConversation, rawRequest: Request):
    await checkForRateLimit("RT:" + rawRequest.client.host, 60, 309)
    await checkForRateLimit("RT:" + req.id, 60, 3099)
    model = await getStoryTeller(req.id)
    conversation = await model.model.memory.getConversation(req.id)
    return conversation
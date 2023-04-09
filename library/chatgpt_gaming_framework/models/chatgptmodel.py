import openai
from ..memory.redismemory import RedisMemory
from ..types.types import Conversation, ConversationList
import uuid
import time

class ChatGPTModel:
    def __init__(self, apikey: str, memory: RedisMemory):
        self.apikey = apikey
        self.model = "gpt-3.5-turbo"
        self.memory = memory
        openai.api_key = self.apikey
        self.chatter = openai.ChatCompletion(self.model)

    async def streamStartConversation(self, newConversationUUID: str, initialMessage: Conversation):
        
        messages = [initialMessage.dict()]
        created = await self.chatter.acreate(
            model = self.model,
            messages = messages,
            stream=True
        )
        fullText = ""
        currentRole = initialMessage.role
        async for item in created:
            firstChoice = item["choices"][0]
            if "delta" in firstChoice and "role" in firstChoice["delta"]:
                currentRole = firstChoice["delta"]["role"]
            if "delta" in firstChoice and "content" in firstChoice["delta"]:
                fullText += item["choices"][0]["delta"]["content"]
                yield {"type": "assitant", "role": currentRole, "content": item["choices"][0]["delta"]["content"]}
            if "text" in firstChoice:
                fullText += item["choices"][0]["text"]
                yield {"type": "assitant", "role": currentRole, "content": item["choices"][0]["text"]}
        messages.append({"role": "assistant", "content": fullText})
        await self.memory.setConversation(newConversationUUID, ConversationList(conversations = messages))
        yield {"type": "stop", "content": newConversationUUID}
            



    async def streamNextStage(self, conversationID: str, newMessage: str, systemMessage: str = None):
        conversation = await self.memory.getConversation(conversationID)
        if len(conversation.conversations) == 0:
            raise Exception("Conversation not found")
        toDict = conversation.dict()
        if systemMessage:
            toDict["conversations"].append({"role": "system", "content": systemMessage})
        toDict["conversations"].append({"role": "user", "content": newMessage})
        created = await self.chatter.acreate(
            model = self.model,
            messages = toDict["conversations"],
            stream=True
        )
        fullText = ""
        messages = conversation.conversations
        messages.append(Conversation(role="user", content=newMessage))
        if systemMessage:
            messages.insert(-1, Conversation(role="system", content=systemMessage))
        currentRole = conversation.conversations[-1].role
        async for item in created:
            firstChoice = item["choices"][0]
            if "delta" in firstChoice and "role" in firstChoice["delta"]:
                currentRole = firstChoice["delta"]["role"]
            if "delta" in firstChoice and "content" in firstChoice["delta"]:
                fullText += item["choices"][0]["delta"]["content"]
                yield {"type": "assitant", "role": currentRole, "content": item["choices"][0]["delta"]["content"]}
            if "text" in firstChoice:
                fullText += item["choices"][0]["text"]
                yield {"type": "assitant", "role": currentRole, "content": item["choices"][0]["text"]}
        messages.append({"role": "assistant", "content": fullText})

        await self.memory.setConversation(conversationID, ConversationList(conversations = messages))


    

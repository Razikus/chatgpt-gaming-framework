from redis.asyncio import Redis
from ..types.types import ConversationList



class RedisMemory:
    def __init__(self, redisurl: str):
        self.redisurl = redisurl
        self.redis = Redis(host = redisurl)

    async def getConversation(self, conversationID: str):
        retrieved = await self.redis.get(f"CONVERSATION:{conversationID}")
        if not retrieved:
            return ConversationList(conversations = [])
        else:
            return ConversationList.parse_raw(retrieved)
        
    async def setConversation(self, conversationID: str, conversation: ConversationList):
        await self.redis.set(f"CONVERSATION:{conversationID}", conversation.json())
        return True
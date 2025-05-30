from openai import AsyncAzureOpenAI
from typing import List, Dict, Any
from ..config import get_settings

settings = get_settings()

class OpenAIService:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT

    async def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error in Azure OpenAI API call: {str(e)}")

    async def create_embedding(self, text: str) -> List[float]:
        try:
            response = await self.client.embeddings.create(
                model=self.deployment,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error in Azure OpenAI embedding API call: {str(e)}") 
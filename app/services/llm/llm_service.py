import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from ..llm.prompts.health_prompts import *
from ..llm.prompts.finance_prompts import *

load_dotenv()

class LLMService:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4")

    async def process_health_data(self, health_data):
        """Process health data and generate insights."""
        prompt = HEALTH_ANALYSIS_PROMPT.format(health_data=health_data)
        response = await self._get_completion(prompt)
        return response

    async def get_health_recommendations(self, health_metrics):
        """Generate health recommendations."""
        prompt = HEALTH_RECOMMENDATION_PROMPT.format(health_metrics=health_metrics)
        response = await self._get_completion(prompt)
        return response

    async def set_health_goals(self, current_data, goals):
        """Generate health goals and action plan."""
        prompt = HEALTH_GOAL_SETTING_PROMPT.format(
            current_data=current_data,
            goals=goals
        )
        response = await self._get_completion(prompt)
        return response

    async def process_finance_data(self, finance_data):
        """Process finance data and generate insights."""
        prompt = FINANCE_ANALYSIS_PROMPT.format(finance_data=finance_data)
        response = await self._get_completion(prompt)
        return response

    async def get_finance_recommendations(self, finance_metrics):
        """Generate finance recommendations."""
        prompt = FINANCE_RECOMMENDATION_PROMPT.format(finance_metrics=finance_metrics)
        response = await self._get_completion(prompt)
        return response

    async def set_finance_goals(self, current_data, goals):
        """Generate finance goals and action plan."""
        prompt = FINANCE_GOAL_SETTING_PROMPT.format(
            current_data=current_data,
            goals=goals
        )
        response = await self._get_completion(prompt)
        return response

    async def _get_completion(self, prompt):
        """Get completion from Azure OpenAI."""
        try:
            response = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are JARVIS, a helpful personal assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting completion: {e}")
            return None 
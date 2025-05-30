from typing import Dict, Any, List
import aiohttp
from ..config import get_settings

settings = get_settings()

class N8NService:
    def __init__(self):
        self.base_url = settings.N8N_WEBHOOK_URL
        self.api_key = settings.N8N_API_KEY

    async def trigger_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger an N8N workflow with the given data
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "X-N8N-API-KEY": self.api_key,
                    "Content-Type": "application/json"
                }
                
                async with session.post(
                    f"{self.base_url}/webhook/{workflow_id}",
                    json=data,
                    headers=headers
                ) as response:
                    if response.status != 200:
                        raise Exception(f"N8N workflow failed with status {response.status}")
                    
                    return await response.json()
                    
        except Exception as e:
            raise Exception(f"Error triggering N8N workflow: {str(e)}")

    async def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """
        Get the status of a workflow execution
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "X-N8N-API-KEY": self.api_key
                }
                
                async with session.get(
                    f"{self.base_url}/executions/{execution_id}",
                    headers=headers
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to get workflow status: {response.status}")
                    
                    return await response.json()
                    
        except Exception as e:
            raise Exception(f"Error getting workflow status: {str(e)}")

    async def get_workflow_data(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get workflow data and configuration
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "X-N8N-API-KEY": self.api_key
                }
                
                async with session.get(
                    f"{self.base_url}/workflows/{workflow_id}",
                    headers=headers
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to get workflow data: {response.status}")
                    
                    return await response.json()
                    
        except Exception as e:
            raise Exception(f"Error getting workflow data: {str(e)}") 
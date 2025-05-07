import requests
import json
from typing import Dict, Any, List

class StabilityAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v1/generation"
    
    def generate_image(self, 
                     prompt: str, 
                     model: str = "stable-diffusion-xl-1024-v1-0",
                     steps: int = 30,
                     cfg_scale: int = 7,
                     width: int = 512,
                     height: int = 512,
                     **kwargs) -> List[Dict[str, Any]]:
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        
        data = {
            "text_prompts": [{"text": prompt}],
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": width,
            "height": height,
            **kwargs
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/{model}/text-to-image",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                error_msg = self._parse_error(response)
                raise Exception(f"API Error: {error_msg}")
                
            return response.json().get('artifacts', [])
            
        except requests.exceptions.RequestException as req_err:
            raise Exception(f"Request failed: {str(req_err)}")
    
    def _parse_error(self, response) -> str:
        """Parse detailed error message from response"""
        try:
            error_data = response.json()
            return f"{error_data.get('name', 'Unknown')}: {error_data.get('message', 'No details')}"
        except:
            return f"Status {response.status_code}: {response.text[:200]}"
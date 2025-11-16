from typing import Dict
from pydantic import BaseModel

class ProviderConfig(BaseModel):
    deployment_name_router: str
    deployment_name_default: str
    api_version: str

class AppConfig(BaseModel):
    active_llm_provider: str
    providers: Dict[str, ProviderConfig]


from pydantic import BaseModel


class DamageData(BaseModel):
    
    timestamp: str
    attack_id : str
    entity_id: str
    result: str
from pydantic import BaseModel


class AttackData(BaseModel):
    
    timestamp: str
    attack_id : str
    entity_id: str
    weapon_type: str
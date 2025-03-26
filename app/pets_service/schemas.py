from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class PetSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"

class PetSpecies(str, Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    FISH = "fish"
    RODENT = "rodent"
    REPTILE = "reptile"
    AMPHIBIAN = "amphibian"
    OTHER = "other"
    
class PetTemperament(str, Enum):
    CALM = "calm"
    FRIENDLY = "friendly"
    PLAYFUL = "playful"
    SHY = "shy"
    AGGRESSIVE = "aggressive"
    ENERGETIC = "energetic"
    INDEPENDENT = "independent"
    SOCIAL = "social"
    PROTECTIVE = "protective"
    CURIOUS = "curious"

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class PetBase(BaseModel):
    name: str
    breed: Optional[str] = None
    species: PetSpecies
    size: Optional[PetSize] = None
    temperament: PetTemperament
    category_id: Optional[int] = None

class PetCreate(PetBase):
    pass

class PetRead(PetBase):
    id: int
    category: Optional[CategoryRead] = None

    class Config:
        orm_mode = True
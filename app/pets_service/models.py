from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum, auto

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

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    
    pets: List["Pet"] = Relationship(back_populates="category")

class Pet( SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    breed: Optional[str] = None
    
    species: PetSpecies
    size: Optional[PetSize] = None
    temperament:PetTemperament
    
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="pets")
    
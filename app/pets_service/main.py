from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select
from models import Category, Pet    # Importe os modelos conforme sua estrutura
from schemas import CategoryCreate, CategoryRead, PetCreate, PetRead  # Importe os schemas conforme sua estrutura
from database import async_session, engine  # Importe as funções e objetos do banco de dados

app = FastAPI()

# Dependência para obtenção da sessão do banco de dados
async def get_db():
    async with async_session() as session:
        yield session

# Evento de startup para criação das tabelas
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Endpoints para Categories

@app.get("/categories/{category_id}", response_model=CategoryRead)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    db_category = result.scalars().first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found.")
    return db_category

@app.get("/category/", response_model=List[CategoryRead])
async def get_categories( db: AsyncSession = Depends(get_db)):
    query = select(Category)
    result = await db.execute(query)
    category = result.scalars().all()
    return category

@app.post("/categories/", response_model=CategoryRead)
async def create_category(category_data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.name == category_data.name))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with given name already exists."
        )
    db_category = Category(**category_data.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


@app.get("/pets/{pet_id}", response_model=PetRead)
async def get_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    db_pet = result.scalars().first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado.")
    return db_pet

@app.get("/pets/", response_model=List[PetRead])
async def get_pets(category_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Pet)
    if category_id is not None:
        query = query.where(Pet.category_id == category_id)
    result = await db.execute(query)
    pets = result.scalars().all()
    return pets

@app.post("/pets/", response_model=PetRead)
async def create_pet(pet_data: PetCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.name == pet_data.name))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pet com este nome já existe."
        )
    db_pet = Pet(**pet_data.dict())
    db.add(db_pet)
    await db.commit()
    await db.refresh(db_pet)
    return db_pet

# Rota raiz
@app.get("/")
def root():
    return {"message": "Welcome to Petmatch"}

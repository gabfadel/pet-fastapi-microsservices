from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to API Gateway"}

@app.get("/pets")
async def get_pets():
    # Roteia a requisição para o pets-service
    async with httpx.AsyncClient() as client:
        response = await client.get("http://pets-service:8000/pets")
    return response.json()

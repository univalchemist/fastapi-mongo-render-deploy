import os
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import uuid
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB: str = os.getenv("MONGODB_DB", "test_coords")

app = FastAPI(
    title="Coordinates API",
    description="API for managing geographic coordinates with MongoDB Atlas",
    version="1.0.0"
)

# MongoDB connection
client: AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB]

# Pydantic models
class CoordinateBase(BaseModel):
    lat: float = Field(..., description="Latitude in decimal degrees format", ge=-90, le=90)
    lng: float = Field(..., description="Longitude in decimal degrees format", ge=-180, le=180)
    notes: Optional[str] = Field(None, description="Optional notes about the location")

class CoordinateCreate(CoordinateBase):
    pass

class Coordinate(CoordinateBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Routes
@app.post("/coordinates/", response_model=Coordinate, status_code=201)
async def create_coordinate(coordinate: CoordinateCreate) -> Coordinate:
    coordinate_dict = coordinate.model_dump()
    coordinate_dict.update({
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    result = await db.coords_data.insert_one(coordinate_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create coordinate")
    
    return coordinate_dict

@app.get("/coordinates/{coordinate_id}", response_model=Coordinate)
async def get_coordinate(coordinate_id: str) -> Coordinate:
    coordinate = await db.coords_data.find_one({"id": coordinate_id})
    if not coordinate:
        raise HTTPException(status_code=404, detail="Coordinate not found")
    return coordinate

@app.get("/coordinates/", response_model=List[Coordinate])
async def list_coordinates() -> List[Coordinate]:
    coordinates = await db.coords_data.find().to_list(length=100)
    return coordinates

@app.put("/coordinates/{coordinate_id}", response_model=Coordinate)
async def update_coordinate(coordinate_id: str, coordinate: CoordinateCreate) -> Coordinate:
    update_data = coordinate.model_dump()
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.coords_data.update_one(
        {"id": coordinate_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Coordinate not found")
    
    updated_coordinate = await db.coords_data.find_one({"id": coordinate_id})
    return updated_coordinate

@app.delete("/coordinates/{coordinate_id}", status_code=204)
async def delete_coordinate(coordinate_id: str) -> None:
    result = await db.coords_data.delete_one({"id": coordinate_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Coordinate not found") 
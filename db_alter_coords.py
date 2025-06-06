import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio
from dotenv import load_dotenv
from typing import NoReturn

load_dotenv()

MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB: str = os.getenv("MONGODB_DB", "test_coords")

async def setup_database() -> None:
    # Connect to MongoDB
    client: AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_URI)
    
    # Get database
    db = client[MONGODB_DB]
    
    # Create collection with schema validation if not exists
    if 'coords_data' not in await db.list_collection_names():
        await db.create_collection('coords_data')
    
    # Create indexes
    await db.coords_data.create_index('lat')
    await db.coords_data.create_index('lng')
    
    # Create schema validation
    await db.command({
        'collMod': 'coords_data',
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['id', 'lat', 'lng', 'created_at', 'updated_at'],
                'properties': {
                    'id': {
                        'bsonType': 'string',
                        'description': 'Primary key - must be a string'
                    },
                    'notes': {
                        'bsonType': 'string',
                        'description': 'Optional notes field'
                    },
                    'lat': {
                        'bsonType': 'double',
                        'description': 'Latitude in decimal degrees format',
                        'minimum': -90,
                        'maximum': 90
                    },
                    'lng': {
                        'bsonType': 'double',
                        'description': 'Longitude in decimal degrees format',
                        'minimum': -180,
                        'maximum': 180
                    },
                    'created_at': {
                        'bsonType': 'date',
                        'description': 'Creation timestamp'
                    },
                    'updated_at': {
                        'bsonType': 'date',
                        'description': 'Last update timestamp'
                    }
                }
            }
        }
    })
    
    print("Database and collection setup completed successfully!")

def main() -> NoReturn:
    asyncio.run(setup_database())

if __name__ == "__main__":
    main() 
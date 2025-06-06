# Coordinates API

A FastAPI application for managing geographic coordinates with MongoDB Atlas integration.

## Features

- RESTful API for managing geographic coordinates
- MongoDB Atlas integration
- Input validation for coordinates
- Automatic API documentation
- Development and production configurations
- Type hints and modern Python features

## Prerequisites

- Python 3.11+
- MongoDB Atlas account
- Git

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create and activate virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```
Edit `.env` and add your MongoDB Atlas connection string:
```
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DB=test_coords
```

## Setup Database

Run the database setup script:
```bash
python db_alter_coords.py
```

## Running the Application

### Development Mode
```bash
python uvicorn_config.py
```

### Production Mode
```bash
python uvicorn_config.py prod
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `POST /coordinates/` - Create a new coordinate
- `GET /coordinates/` - List all coordinates
- `GET /coordinates/{coordinate_id}` - Get a specific coordinate
- `PUT /coordinates/{coordinate_id}` - Update a coordinate
- `DELETE /coordinates/{coordinate_id}` - Delete a coordinate

## Data Format

Coordinates are stored in decimal degrees (DD) format:
- Latitude (lat): -90 to 90
- Longitude (lng): -180 to 180

Example request body:
```json
{
    "lat": 25.7617,
    "lng": -80.1918,
    "notes": "Optional notes about the location"
}
```

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes

### Git Workflow
1. Create a new branch for features/fixes
2. Make your changes
3. Write tests if applicable
4. Submit a pull request

## License

[Your chosen license]

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 
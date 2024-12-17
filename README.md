# Voker Dupe Plus API Generator

## Prerequisites

- **Python**: Python 3.12.6 or higher
- **Dependencies**: Install the required dependencies using:
  ```bash
  pip install fastapi openai pydantic uvicorn
  ```
- **Set Openai api Keys**
  ```bash
   export OPENAI_API_KEY=your_openai_api_key
  ```

## Getting Started
1. **Clone Repository**
```bash
git clone https://github.com/your-repo/voker_dupe_plus.git
cd voker_dupe_plus/api
```
2. **Start Server**
```bash
uvicorn voker_dupe:app --reload
```
3. **Create Your own API** (Example)
```json
{
  "api_name": "Apartment_hunter",
  "input": {
    "instructions": "Provide apartments based on city_location and describe features.",
    "input_vars": [
      {
        "var_name": "City_name",
        "description": "Los Angeles"
      }
    ]
  },
  "output": {
    "output_vars": [
      {
        "var_name": "Apartment_name",
        "description": "Name of Apartment in the input city"
      },
      {
        "var_name": "Features",
        "description": "Description of Apartment, include amenities, room sizes, etc"
      }
    ]
  }
}
```
4. Make the Endpoint
```bash
curl -X POST "http://localhost:8000/generate_api/" -H "Content-Type: application/json" -d '{
  "api_name": "Apartment_hunter",
  "input": {
    "instructions": "Provide apartments based on city_location and describe features.",
    "input_vars": [
      {
        "var_name": "City_name",
        "description": "Los Angeles"
      }
    ]
  },
  "output": {
    "output_vars": [
      {
        "var_name": "Apartment_name",
        "description": "Name of Apartment in the input city"
      },
      {
        "var_name": "Features",
        "description": "Description of Apartment, include amenities, room sizes, etc"
      }
    ]
  }
}'
```
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Callable
from openai import api_key
from openai import OpenAI
import os

app = FastAPI()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
class APIVariable(BaseModel):
    var_name: str = Field(..., description="Variable Name")
    description: str = Field(..., description="A description of the Variable")
    
class Input(BaseModel):
    instructions: str
    input_vars: list[APIVariable]
    
class Output(BaseModel):
    output_vars: list[APIVariable]
    
class API(BaseModel):
    api_name: str
    input: Input
    output: Output
    
def api_model(instructions: str, input: Input, output: Output) -> str:
    sys_prompt = """You are an agent that 
    recieves a set of instructions, 
    input variables, and output variables. Follow instructions
    based on input variables and focus your output
    on things related to the output variables and their descriptions"""
    usr_prompt = f"Instructions: {instructions}\nInput Variables:\n"
    for i in input:
        usr_prompt += f"{i.var_name}: {i.description}\n"
    usr_prompt += f"Output Variables:\n"
    for o in output:
        usr_prompt += f"{o.var_name}: {o.description}\n"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role":"system", "content": sys_prompt},
            {"role": "user", "content": usr_prompt},
        ]
    )
    
    result = response.choices[0].message
    return result
    
    
example_data = {
    "api_name": "Apartment-Hunter",
    "input": {
        "instructions": "Give me apartments based on @city_location and tell me some of the good qualities these apartments have",
        "input_vars": [
        {"var_name": "City_location", "description": "Los Angeles"},]
    },
    "output": {
        "output_vars": [
            {"var_name": "Features", "description": "Description of Apartment, include amenities, room sizes, etc"},
            {"var_name": "ApartmentName", "description": "Name of Apartment in the input city"}    
        ],
    }
}


api = API(**example_data)

out = api_model(api.input.instructions, api.input.input_vars, api.output.output_vars)
print(out)



# def create_endpoint(app: FastAPI, endpoint_description: Dict[str, any]):
    
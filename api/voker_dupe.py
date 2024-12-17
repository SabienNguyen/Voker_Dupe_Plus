from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI
from typing import List, Dict, Any, Optional
import os

app = FastAPI()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
class APIVariable(BaseModel):
    var_name: str = Field(..., description="Variable Name")
    description: Optional[str] = Field(None, description="A description of the Variable")
    
class Input(BaseModel):
    instructions: str
    input_vars: list[APIVariable]
    
class Output(BaseModel):
    output_vars: list[APIVariable]
    
class API(BaseModel):
    api_name: str
    input: Input
    output: Output
    
generated_apis:Dict[str, Any] = {}
    
def api_model(instructions: str, input: Input, output: Output) -> str:
    sys_prompt = """You are an agent that 
    recieves a set of instructions, 
    input variables, and output variables. Follow instructions
    based on input variables and focus your output
    on things related to the output variables and their descriptions"""
    usr_prompt = f"Instructions: {instructions}\nInput Variables:\n"
    for i in input.input_vars:
        usr_prompt += f"{i.var_name}: {i.description}\n"
    usr_prompt += f"Output Variables:\n"
    for o in output.output_vars:
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
    

@app.post("/generate_api/")
async def generate_api(api: API):
    if api.api_name in generated_apis:
        raise HTTPException(status_code=400, detail="API name already exists.")
    
    generated_apis[api.api_name] = {
        "input_vars": api.input.input_vars,
        "output_vars": api.output.output_vars,
        "instructions": api.input.instructions,
    }
    
    async def dynamic_endpoint(payload: Dict):
        required_vars = {var.var_name for var in api.input.input_vars}
        if not required_vars.issubset(payload.keys()):
            raise HTTPException(status_code=400, detail=f"Missing required input variables: {required_vars}")
        
        result = api_model(api.input.instructions, api.input, api.output)
        return {"api_name": api.api_name, "output": result}
    
    endpoint_path = f"/api/{api.api_name}"
    app.add_api_route(endpoint_path, dynamic_endpoint, methods=["POST"])
    
    return {
        "message": "API generated successfully!",
        "endpoint_url": f"http://localhost:8000{endpoint_path}"
    }

@app.get("/api/{api_name}")
async def get_api(api_name: str):
    if api_name in generated_apis:
        return {"message": f"API {api_name} accessed successfully!"}
    else:
        raise HTTPException(status_code=404, detail="API not found")

@app.get("/list_apis/")
async def list_apis():
    return {"generated_apis": list(generated_apis.keys())}
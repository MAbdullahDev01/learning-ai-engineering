from fastapi import FastAPI
from pydantic import BaseModel, PositiveInt

class AgentMetadata(BaseModel):
    name : str 
    role : str
    max_tokens : PositiveInt
    tools : list[str]

class SimulationRequest(BaseModel):
    agent_config: AgentMetadata
    user_input: str

class AIAgent:
    def __init__(self, agent_data : AgentMetadata) -> None:
        self.metadata = agent_data

    def get_full_prompt(self, user_input : str) -> str:
        system_prompt : str = f"Your name is {self.metadata.name}. You must act strictly as a {self.metadata.role}. Do not break character, and tailor all your responses to fit this specific role. You have a strict response budget. You must ensure your entire answer fits comfortably within a maximum limit of {self.metadata.max_tokens} tokens. Be concise, direct, and do not waste tokens on unnecessary pleasantries. You have access to the following tools: {self.metadata.tools}."

        return system_prompt + "\n\n" + user_input

app = FastAPI()

@app.post("/simulate-agent")
def input_metadata(payload : SimulationRequest):
    agent = AIAgent(agent_data = payload.agent_config)
    compiled_prompt = agent.get_full_prompt(user_input = payload.user_input)

    return {
        "status": "success",
        "agent_initialized": payload.agent_config.name,
        "full_prompt": compiled_prompt
    }

class AgentConfig:

    def __init__(self, model_name, parent_company) -> None:
        
        self.model_name =  model_name
        self.parent_company = parent_company
    
    def describe_settings(self) -> str:
        return(f"{self.model_name} owned by {self.parent_company}.")
    
model_config = AgentConfig("GPT-5.6 Luna", "OpenAI")
print(model_config.describe_settings())
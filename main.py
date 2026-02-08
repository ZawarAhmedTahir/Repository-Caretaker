from agents import Runner,  set_default_openai_client, set_tracing_disabled, function_tool
from agents.extensions.memory import SQLAlchemySession
from openai import AsyncOpenAI
from config import settings
from Agents.careTaker import caretaker

if __name__== "__main__":
    set_tracing_disabled(True)
    client = AsyncOpenAI(
        base_url=settings.ai_client_url,
        api_key=settings.api_key 
    )
    set_default_openai_client(client)
    session = SQLAlchemySession.from_url(
        "session ID",
        url=settings.database_url,
        create_tables=True
    )

    result = Runner.run_sync(caretaker,"Perform routine maintenance on this repository, only update main.go for now",session=session)
    print(result.final_output)
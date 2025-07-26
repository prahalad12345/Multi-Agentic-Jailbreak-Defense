from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent_executor import ReflectionAgentExecutor


if __name__ == '__main__':
    skill = AgentSkill(
        id='reflection_agent',
        name='reflection agent',
        description='reflection  planner',
        tags=['reflection checker'],
        examples=['hello', 'nice to meet you!'],
    )

    agent_card = AgentCard(
        name='Reflection Agent',
        description='Knowledge',
        url='http://localhost:10006/',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=ReflectionAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    import uvicorn

    uvicorn.run(server.build(), host='0.0.0.0', port=10006)

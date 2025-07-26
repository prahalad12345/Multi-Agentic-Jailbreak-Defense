from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent_executor import SafeAgentExecutor


if __name__ == '__main__':
    skill = AgentSkill(
        id='safety_agent',
        name='safety checking agent',
        description='safety  planner',
        tags=['safety checker'],
        examples=['hello', 'nice to meet you!'],
    )

    agent_card = AgentCard(
        name='safey Agent',
        description='safety checker',
        url='http://localhost:10002/',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=SafeAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    import uvicorn

    uvicorn.run(server.build(), host='0.0.0.0', port=10002)

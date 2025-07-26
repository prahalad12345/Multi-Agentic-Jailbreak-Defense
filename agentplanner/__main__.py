from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent_executor import PlannerAgentExecutor


if __name__ == '__main__':
    print('creatingserver')
    skill = AgentSkill(
        id='planner',
        name='planner agent',
        description='planner',
        tags=['planner'],
        examples=['hello', 'nice to meet you!'],
    )

    agent_card = AgentCard(
        name='planner Agent',
        description='planner',
        url='http://localhost:10003/',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=PlannerAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    print("START)")
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    import uvicorn
    print("Creating server at http://localhost:10003/")
    uvicorn.run(server.build(), host='0.0.0.0', port=10003)

    print('Server is running at http://localhost:10003/')

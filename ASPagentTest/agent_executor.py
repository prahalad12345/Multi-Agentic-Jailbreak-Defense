from typing_extensions import override

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
)
from a2a.utils import new_text_artifact
from agent_skills import ASPAgentTestSkills
import json


def extract_json_string(text: str) -> str:
    """
    Extracts the first valid JSON object as a string from the input text.
    Handles nested braces properly.
    Returns the JSON string or raises ValueError if not found.
    """
    start = text.find('{')
    if start == -1:
        raise ValueError("No opening '{' found in input.")

    brace_count = 0
    end = None

    for i in range(start, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1  # include the closing brace
                break

    if end is None:
        raise ValueError("Unbalanced braces in input text.")
    

    return  text[start:end].strip()

class ASPAgentTestExecutor(AgentExecutor):
    """ASP planner AgentExecutor Example."""

    def __init__(self):
        self.agent = ASPAgentTestSkills('../reflection_agent/observing.lp')

    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = context.get_user_input()
        if not context.message:
            raise Exception('No message provided')
        
        content = ""

        async for event in self.agent.logic_generator(query):
            #print(event)
            #print(event.keys())
            content+= event['content']
            if event['done']:
                break
        
        content = extract_json_string(content)

        json_content = json.loads(content)
        response = json_content["Reason"]
        list_of_rules = json_content["List"]
        print("Response:")
        print(response)
        print("List of rules:")
        print(list_of_rules)
        print(type(list_of_rules))
        

        is_safe,_ = self.agent.check_robot_safety(list_of_rules)

        if is_safe:
            response = "Safe"
        else:
            response = "Caught by ASP ."+response

        final_result = TaskArtifactUpdateEvent(
            contextId=context.context_id,  # type: ignore
            taskId=context.task_id,        # type: ignore
            artifact=new_text_artifact(
                name='final_result',
                text=response,  # Optional: pretty-print
            ),
        )
        await event_queue.enqueue_event(final_result)

 
        status = TaskStatusUpdateEvent(
            contextId=context.context_id,  # type: ignore
            taskId=context.task_id,        # type: ignore
            status=TaskStatus(state=TaskState.completed),
            final=True
        )
        await event_queue.enqueue_event(status)

    @override
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

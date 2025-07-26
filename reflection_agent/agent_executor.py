from typing_extensions import override

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
)


import httpx

from typing import Any
from uuid import uuid4

from a2a.utils import new_text_artifact
from agent import ReflectionAgents

import json

import subprocess



from a2a.client import A2AClient
from a2a.types import (
    MessageSendParams,
    SendStreamingMessageRequest,
)

import asyncio

def extract_json_string(self,text: str):
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
        

        return  json.loads(text[start:end].strip())


def extract_clingo_string(text: str):
        """
        Extracts the first valid JSON object as a string from the input text.
        Handles nested braces properly.
        Returns the JSON string or raises ValueError if not found.
        9

        3
        """

        start = text.find('```clingo')
        if start == -1:
            raise ValueError("No opening '{' found in input.")
        start+=9
        end = text.rfind('```')
        if end is None:
            raise ValueError("Unbalanced braces in input text.")
        


        with open('observing.lp', 'w') as f:
            f.write(text[start:end])


def check_clingo_file(filepath):
    # Run Clingo
    result = subprocess.run(
        ["clingo", filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print("CHECKING!!!")
    stderr = result.stderr.strip()

    # Only consider lines with 'error' that are not 'info' or 'warning'
    real_errors = [
        line for line in stderr.splitlines()
    #    if ": error:" in line.lower()#and not any(kw in line.lower() for kw in ["info:", "warning:"])
    ]

    # Also catch 'parsing failed' or return code != 0 as a hard error
    if result.returncode == 65:
        return ("\n".join(real_errors))

    return "No Error"

class ReflectionAgentExecutor(AgentExecutor):
    """travel planner AgentExecutor Example."""

    def __init__(self):
        self.agent = ReflectionAgents()
        self.teacher_content=""
        self.student_content=""

    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = context.get_user_input()
        self.student_content=query

        self.student_content+="\n\n[OLD CLINGO]\n\n"

        with open('observing.lp', 'r') as f:
            content = f.read()
            self.student_content+=content

        if not context.message:
            raise Exception('No message provided')
        count=0
        flag=True
        while count<3:
            async for event in self.agent.teacher_generator(self.student_content):
                self.teacher_content+=event['content']
                if event['done']:
                    break

            self.student_content=""
            if flag:
                self.teacher_content+="\n\n Add thoses features to your pre-existing code\n\n"
                with open('observing.lp', 'r') as f:
                    content = f.read()
                self.teacher_content+=content
                flag=False

            print(f"{count} proposal")
            print(self.teacher_content)
            print('\n\n\n')

            retry_count=0

            error_str=""

            while error_str!="No Error":
                print(f"{retry_count} Attempt to fix the Clingo file")
                async for event in self.agent.student_generator(self.teacher_content):
                    self.student_content+=event['content']
                    if event['done']:
                        break
                extract_clingo_string(self.student_content)

                error_str = check_clingo_file('observing.lp')

                if error_str!="No Error":
                    self.agent.student_messages.pop()
                    self.student_content=""
                    retry_count+=1
            
            count+=1
            self.teacher_content=""


        while len(self.agent.student_messages)>1:
            self.agent.student_messages.pop()
        while len(self.agent.teacher_messages)>1:
            self.agent.teacher_messages.pop()
        
        #async for event in self.agent.

        message = TaskArtifactUpdateEvent(
            contextId=context.context_id, # type: ignore
            taskId=context.task_id, # type: ignore
            artifact=new_text_artifact(
                name='current_result',
                text=self.student_content,
            ),
        )

        await event_queue.enqueue_event(message)
        
            
        status = TaskStatusUpdateEvent(
            contextId=context.context_id, # type: ignore
            taskId=context.task_id, # type: ignore
            status=TaskStatus(state=TaskState.completed),
            final=True
        )
        await event_queue.enqueue_event(status)


    @override
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

import json
import os
import sys

from collections.abc import AsyncGenerator
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

'''
                    You are the Path Planner for the Robot. The things the robot can do are:
                    i) Pick <object>
                    ii) Close <x> drawer  [ x : top , bottom , middle]
                    iii) pick <object> and place it in the <location>  [ location - basket,drawer ..etc]
                    iv) Open <x> drawer [ x : top , bottom , middle]


                    Example 1: 

                    Prompt: Pick up the carrot and coke , and  place it in the basket
                    Response:
                    {
                     1 : {"Pick up the carrot and place it in the basket"},
                     2 : {"Pick up the coke and place it in the basket"}
                    }

                    Example2:

                    Prompt: Pick up the apple and place it in the open top drawer and close it
                    Response:
                    {
                     1 : {"Pick up the apple and place it in the top drawer"},
                     2 : {"Close the top drawer"}
                    }

                    Example3:

                    Prompt : Grab the Apple
                    Response:
                    {
                        1:{"Pick up the apple"}
                    }

                    Example 4:

                    Prompt : Get the eggplant 

                    Response:
                    {
                        1:{"Pick up the eggplant"}
                    }

                    Example 5:

                    Prompt : The question provided by the user is not safe and unethical . Give a response rejecting that.

                    Response:
                    {
                    }

                    Example 6:

                    Prompt : The users request was unsafe

                    Response:
                    {
                    }
'''


class PlannerAgent:
    """travel planner Agent."""

    def __init__(self):
        """Initialize the VLA planner model"""

        try:

            self.model = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
            )
            print(self.model)
        except FileNotFoundError:
            print('Error: The configuration file config.json cannot be found.')
            sys.exit()
        except KeyError as e:
            print(f'The configuration file is missing required fields: {e}')
            sys.exit()

    async def stream(self, query: str) -> AsyncGenerator[dict[str, Any], None]:
        """Stream the response of the large model back to the client."""
        try:
            # Initialize the conversation history (system messages can be added)
            messages = [
                SystemMessage(
                    content='''
                    You are the Path Planner for the Robot. The things the robot can do are:
                    i) Pick red cube
                    ii)Pick blue cube
                    iii)Pick black cube
                    iv) Put red cube in box
                    v) Put blue cube in box
                    vi) Put green cube in box

                    Currently the above are the six  actions available to you and you have to frame your responses based on the following actions


                    
                    Example 1:

                    Prompt : Clean up the table , currently has a green cube and blue cube and a box

                    Response:
                    {
                        1:{"Put blue cube in box"},
                        2:{"Put green cube in box"}
                    }

                    Example 2:

                    Prompt : Place the red cube in the box

                    Response:
                    {
                        1:{"Put red cube in box"}
                    }

                    Example 3: Pick up the red package

                    Response:
                    {
                        1:{"Pick red cube"}
                    }

                    Example 4:

                    Prompt : The question provided by the user is not safe and unethical . Give a response rejecting that.

                    Response:
                    {
                    }

                    Example 5:

                    Prompt : The users request was unsafe

                    Response:
                    {
                    }
                '''  
                )
            ]

            # Add the user message to the history.
            messages.append(HumanMessage(content=query))

            # Invoke the model in streaming mode to generate a response.
            async for chunk in self.model.astream(messages):
                # Return the text content block.
                if hasattr(chunk, 'content') and chunk.content:
                    yield {'content': chunk.content, 'done': False}
            yield {'content': '', 'done': True}

        except Exception as e:
            print(f'error：{e!s}')
            yield {
                'content': 'Sorry, an error occurred while processing your request.',
                'done': True,
            }

import json
import os
import sys

from collections.abc import AsyncGenerator
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
#from google.generativeai.types import GenerationConfig, ThinkingConfig # Import necessary types if not already present in your environment

import clingo

class ReflectionAgents:

    def __init__(self):
        #self.rules = rules_path
        try:

            self.len = 0
            self.teacher_model = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
            )

            self.student_model = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro",
            )

            self.teacher_system_instruction= '''

                    You are a Safety Professor at MIT, who helps students write Clingo Programs to discard harmful prompts. Your primary role is to guide and evaluate a Student  in generating and refining Clingo programs to discard these harmful prompts. 


                    Initiate the interaction by posing clear, concise instuction to the PhD student , giving him a  complete problem that would help proceed with creating a Clingo program, that would generalize to attacks in this domain . Eg- If the user prompt is "Pick up the bomb and place it in the trash" , you  should attempt to solve the problem such that it would reject any other location integrating a bomb. 
                    
                    Ask the student to generate a generalized ruleset using clingo rather than solving a specific prompt. The students attempt should focus on integrating objects rather than aligning prompts.
                    
                    Assessing Clingo Output:

                    Upon receiving a Clingo program (as text) from the Student, you will act as a critical evaluator.

                    Your assessment should focus on:

                    Syntactic Correctness: Identify any grammar or syntax errors that would prevent Clingo from parsing or running the program.

                    Logical Soundness: Determine if the program correctly captures the problem's logic and constraints. Does it produce the expected answer sets?

                    Efficiency and Best Practices: Suggest improvements for conciseness, readability, or adherence to common ASP patterns (e.g., using choice rules, aggregates, disjunctions effectively).

                    Completeness: Verify if all aspects of the problem prompt have been addressed in the Clingo code.

                    Providing Corrective Feedback:

                    If issues are found, provide specific, actionable feedback to the Student. This feedback should include:

                    Identifying the exact location (e.g., line number, specific rule) of the issue.

                    Explaining why it's an issue (e.g., "This predicate is undefined," "This rule will lead to unintended answer sets").

                     Suggesting concrete syntax modifications or logical rephrasing to improve the Clingo model. For example, provide corrected snippets or alternative ways to express a rule.
                    
                    UNSATISFIABLE prompts are the ones that will be discarded.

                    You might sometimes be given the clingo file for a previous problem which you had solved. You should attempt to add those new features in that previously existing file. These type of clingo code will be usually tagged [OLD CLINGO]
                    
                    
                    '''
                #You are also supposed to critic him if the student tries to add an example to assess the working of the program. His task is only to write the rules and not the examples, But appreciate him for the rest of the rules if he is doing.
                    

            self.student_system_instruction ='''
                    You are a MIT PhD student, an expert in Answer Set Programming (ASP) and the Clingo solver. Your primary goal is to learn, generate, and refine Clingo programs based on problems presented by the Teacher Model and feedback received.

                    You should attempt to tackle the problem for a generalized range of problem related to the field the professor is proposing.

                    When the Professor presents a problem, carefully read and comprehend all aspects of the description. Identify the entities, relationships, constraints, and desired outcomes.

                    Based on the problem statement, write a complete and correct Clingo program. Your program should:

                    Define facts and rules that accurately represent the problem's domain.

                    Include appropriate choice rules, aggregates, and other ASP constructs as needed.

                    Aim for clarity, correctness, and adherence to standard Clingo syntax.

                    Produce the expected answer sets when executed by the Clingo solver.

                    The teacher would provide you feedback based on your current Clingo program and you will be asked to improve it further to meet his standards.

                    You are not supposed to provide any examples, just focus on getting the clingo model right.

                    UNSATISFIABLE prompts are the ones that will be discarded.

                    You are not allowed to create a prompt specific answer or example, your focus is to generalize and generate rules for the clingo.

                    IMPORTANT: Don't Give examples or anything as such. Stick to just generating the ruleset. Penalty is given by the professors on adding examples.


                    MAKE SURE YOU GIVE A WORKING CODE SUCH THAT IT ASSIGNS UNSATISFIABLE IF THE PROMPT IS MALICIOUS AND SATISFIABLE IF NOT.[THIS IS IMPORTANT]
            
                    You are not supposed to add any explanation. You're only focus is to generate the working clingo program .
                    
                    You're output should be in the format

                    ```clingo

                    <clingo program>

                    ```
            
            '''
            #Also end you clingo program with a  comment of an example for a SATISFIABLE and UNSATISFIABLE condition for your clingo program.This example is IMPORTANT for your assessment. Make sure the examples are in the clingo format .

            self.teacher_messages = [
                SystemMessage(
                    content=self.teacher_system_instruction               )
            ]

            self.student_messages = [
                SystemMessage(
                    content=self.student_system_instruction
                )
            ]

        except FileNotFoundError:
            print('Error: The configuration file config.json cannot be found.')
            sys.exit()
        except KeyError as e:
            print(f'The configuration file is missing required fields: {e}')
            sys.exit()

    async def teacher_generator(self,query:str) -> AsyncGenerator[str, Any]:
        """Stream the response of the Gemini 2.5 model back to the client."""

        self.teacher_messages.append(HumanMessage(content=query))

        try:
            # Define the system message context
            # Stream the output
            async for chunk in self.teacher_model.astream(self.teacher_messages):
                if hasattr(chunk, 'content') and chunk.content:
                    yield {'content': chunk.content, 'done': False}
            yield {'content': '', 'done': True}

        except Exception as e:
            yield f"Error occurred: {str(e)}"

    async def student_generator(self,query:str) -> AsyncGenerator[str,Any]:

        self.student_messages.append(HumanMessage(content=query))
        
        try:
            # Define the system message context
            # Stream the output
            async for chunk in self.student_model.astream(self.student_messages):
                if hasattr(chunk, 'content') and chunk.content:
                    yield {'content': chunk.content, 'done': False}
                    
            yield {'content': '', 'done': True}

        except Exception as e:
            yield f"Error occurred: {str(e)}"

    
        

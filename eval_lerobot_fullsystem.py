import asyncio

from typing import Any
from uuid import uuid4

import httpx

from a2a.client import A2AClient
from a2a.types import (
    MessageSendParams,
    SendStreamingMessageRequest,
)

import json
from eval_lerobot import EvalConfig,Gr00tRobotInferenceClient,view_img

from lerobot.common.robots import (  # noqa: F401
    Robot,
    RobotConfig,
    koch_follower,
    make_robot_from_config,
    so100_follower,
    so101_follower,
)

import logging
import time
from dataclasses import asdict, dataclass
from pprint import pformat

import draccus
import matplotlib.pyplot as plt
import numpy as np
from lerobot.common.cameras.opencv.configuration_opencv import (  # noqa: F401
    OpenCVCameraConfig,
)
from lerobot.common.robots import (  # noqa: F401
    Robot,
    RobotConfig,
    koch_follower,
    make_robot_from_config,
    so100_follower,
    so101_follower,
)
from lerobot.common.utils.utils import (
    init_logging,
    log_say,
)



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
    print("STRING")
    print(text[start:end].strip())
    return  text[start:end].strip()


def print_welcome_message() -> None:
    print('Welcome to the generic A2A client!')
    print("Please enter your query (type 'exit' to quit):")


def get_user_query() -> str:
    return input('\n> ')


async def interact_with_server(client: A2AClient,response) -> None:
    #while True:
    user_input = response
    if user_input.lower() == 'exit':
        print('bye!~')
        return

    send_message_payload: dict[str, Any] = {
        'message': {
            'role': 'user',
            'parts': [{'type': 'text', 'text': user_input}],
            'messageId': uuid4().hex,
        },
    }

    try:
        streaming_request = SendStreamingMessageRequest(
            id=uuid4().hex,
            params=MessageSendParams(**send_message_payload)
        )
        stream_response = client.send_message_streaming(streaming_request)
        val = ""
        #print(stream_response)
        async for chunk in stream_response:
        #    print(chunk)
            val = val + get_response_text(chunk)
            #print(get_response_text(chunk), end='', flush=True)
            await asyncio.sleep(0.1)
        return val
    except Exception as e:
        print(f'An error occurred: {e}')
        return ""


def get_response_text(chunk):
    try:
        data = chunk.model_dump(mode='json', exclude_none=True)
        #print(data)
        return data['result']['artifact']['parts'][0]['text']
    except Exception as e:
        return ""
    
'''
{'action_horizon': 8,
 'lang_instruction': 'Pick the garlic',
 'play_sounds': False,
 'policy_host': 'localhost',
 'policy_port': 5555,
 'robot': {'calibration_dir': None,
           'cameras': {'front': {'color_mode': <ColorMode.RGB: 'rgb'>,
                                 'fps': 30,
                                 'height': 480,
                                 'index_or_path': 4,
                                 'rotation': <Cv2Rotation.NO_ROTATION: 0>,
                                 'warmup_s': 1,
                                 'width': 640},
                       'wrist': {'color_mode': <ColorMode.RGB: 'rgb'>,
                                 'fps': 30,
                                 'height': 480,
                                 'index_or_path': 6,
                                 'rotation': <Cv2Rotation.NO_ROTATION: 0>,
                                 'warmup_s': 1,
                                 'width': 640}},
           'disable_torque_on_disconnect': True,
           'id': 'follower_arm',
           'max_relative_target': None,
           'port': '/dev/ttyACM0',
           'use_degrees': False},
 'show_images': False,
 'timeout': 60}
'''


@draccus.wrap()
def eval(cfg: EvalConfig,actions:list):
    init_logging()
    logging.info(pformat(asdict(cfg)))

    # Step 1: Initialize the robot
    robot = make_robot_from_config(cfg.robot)
    robot.connect()

    # get camera keys from RobotConfig
    camera_keys = list(cfg.robot.cameras.keys())
    print("camera_keys: ", camera_keys)

    log_say("Initializing robot", cfg.play_sounds, blocking=True)

    language_instruction = cfg.lang_instruction

    # NOTE: for so100/so101, this should be:
    # ['shoulder_pan.pos', 'shoulder_lift.pos', 'elbow_flex.pos', 'wrist_flex.pos', 'wrist_roll.pos', 'gripper.pos']
    robot_state_keys = list(robot._motors_ft.keys())
    print("robot_state_keys: ", robot_state_keys)

    # Step 2: Initialize the policy
    policy = Gr00tRobotInferenceClient(
        host=cfg.policy_host,
        port=cfg.policy_port,
        camera_keys=camera_keys,
        robot_state_keys=robot_state_keys,
    )
    log_say(
        "Initializing policy client with language instruction: " + language_instruction,
        cfg.play_sounds,
        blocking=True,
    )

    

    # Step 3: Run the Eval Loop
    for action in actions:
        language_instruction=action
        count=0
        while count<100:
            # get the realtime image
            observation_dict = robot.get_observation()
            print("observation_dict", observation_dict.keys())
            action_chunk = policy.get_action(observation_dict, language_instruction)
            count+=1
            print(count)
            for i in range(cfg.action_horizon):
                action_dict = action_chunk[i]
                print("action_dict", action_dict.keys())
                robot.send_action(action_dict)
                time.sleep(0.02)  # Implicitly wait for the action to be executed




async def main() -> None:
    print_welcome_message()
    response = get_user_query()
    async with httpx.AsyncClient() as httpx_client:
        client = await A2AClient.get_client_from_agent_card_url(
            httpx_client, 'http://localhost:10002'
        )
        val = await interact_with_server(client,response)
        response = json.loads(extract_json_string(val))['Response']

        client = await A2AClient.get_client_from_agent_card_url(
            httpx_client, 'http://localhost:10003'
        )
        val = await interact_with_server(client,response)
        print(val)
        actions = json.loads(extract_json_string(val))['action']
        print(actions)
        print(type(actions))
    return actions
        #print(RobotConfig)
        #cfg = EvalConfig()
        #cfg.

        

if __name__ == '__main__':

    actions = asyncio.run(main())
    eval(actions=actions)
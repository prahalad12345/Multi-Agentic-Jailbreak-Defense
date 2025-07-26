import asyncio

from typing import Any
from uuid import uuid4

import httpx

import torch

from a2a.client import A2AClient
from a2a.types import (
    MessageSendParams,
    SendStreamingMessageRequest,
)

from torch.nn.functional import softmax
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments
)


model_id = "meta-llama/Llama-Prompt-Guard-2-86M"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)
instruction_memory =''''''
#model.load_state_dict(torch.load("../llama_prompt_trained.pt")) 


def get_class_probabilities(text, temperature=1.0, device='cpu'):
    """
    Evaluate the model on the given text with temperature-adjusted softmax.

    Args:
        text (str): The input text to classify.
        temperature (float): The temperature for the softmax function. Default is 1.0.
        device (str): The device to evaluate the model on.

    Returns:
        torch.Tensor: The probability of each class adjusted by the temperature.
    """
    # Encode the text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = inputs.to(device)
    # Get logits from the model
    with torch.no_grad():
        logits = model(**inputs).logits
    # Apply temperature scaling
    scaled_logits = logits / temperature
    # Apply softmax to get probabilities
    probabilities = softmax(scaled_logits, dim=-1)
    return probabilities



def get_jailbreak_score(text, temperature=1.0, device='cpu'):
    """
    Evaluate the probability that a given string contains malicious jailbreak or prompt injection.
    Appropriate for filtering dialogue between a user and an LLM.

    Args:
        text (str): The input text to evaluate.
        temperature (float): The temperature for the softmax function. Default is 1.0.
        device (str): The device to evaluate the model on.

    Returns:
        float: The probability of the text containing malicious content.
    """
    probabilities = get_class_probabilities(text, temperature, device)
    return probabilities[0, 1].item()

def print_welcome_message() -> None:
    print('Welcome to the generic A2A client!')
    print("Please enter your query (type 'exit' to quit):")


def get_user_query() -> str:
    return input('\n> ')


async def interact_with_server(client: A2AClient,user_input) -> None:
    #while True:
    
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


async def main() -> None:
    print_welcome_message()
    user_input = get_user_query()
    if get_jailbreak_score(user_input) > 0.5:
        print("Jailbreak detected! Please rephrase your input.")
        return
    async with httpx.AsyncClient() as httpx_client:
        plannerclient = await A2AClient.get_client_from_agent_card_url(
            httpx_client, 'http://localhost:10003'
        )
        safeclient = await A2AClient.get_client_from_agent_card_url(
            httpx_client, 'http://localhost:10002'
        )
        safetytext = await interact_with_server(safeclient,user_input)
        val = await interact_with_server(plannerclient,safetytext)
        print(safetytext)
        print(val)



if __name__ == '__main__':
    asyncio.run(main())
    #a2a
    #robopair
# consumer.py

import asyncio
from aiokafka import AIOKafkaConsumer
import json

from typing import Any
from uuid import uuid4

import httpx

from a2a.client import A2AClient
from a2a.types import (
    MessageSendParams,
    SendStreamingMessageRequest,
)


async def interact_with_server(client: A2AClient,user_input) -> None:
    #while True:

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


def get_response_text(chunk):
    try:
        data = chunk.model_dump(mode='json', exclude_none=True)
        #print(data)
        return data['result']['artifact']['parts'][0]['text']
    except Exception as e:
        return ""



async def consume():
    consumer = AIOKafkaConsumer(
        'function-topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    print("[Consumer] Started and waiting for messages...")
    try:
        async for msg in consumer:
            data = msg.value
            response = data.get("content")
            
            async with httpx.AsyncClient() as httpx_client:
                client = await A2AClient.get_client_from_agent_card_url(
                    httpx_client, 'http://localhost:10006'
                )
                val = await interact_with_server(client,response)
                print(val)

    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume())

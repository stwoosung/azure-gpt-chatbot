import azure.functions as func
import logging
from openai import OpenAI
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage

import os
import json

app = func.FunctionApp()
client = OpenAI()

servicebus_client = ServiceBusClient.from_connection_string(conn_str=os.environ['SERVICEBUS_CONNECTION_URL'], logging_enable=True)


@app.service_bus_queue_trigger(arg_name="msg", queue_name="process-request-queue",
                               connection="SERVICEBUS_CONNECTION_URL") 
async def process_request(msg: func.ServiceBusMessage):
    
    message = json.loads(msg.get_body().decode('utf-8'))
    response = client.responses.create(
        model="gpt-4.1",
        input=message['content']
    )

    answer_data = {
        "channel_id": message['channel_id'], 
        "content": response.output_text, 
        "type": "answer"
    }

    async with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name="process-response-queue")

        async with sender:
            message = ServiceBusMessage(json.dumps(answer_data))
            await sender.send_messages(message)

    logging.info(response.output_text)

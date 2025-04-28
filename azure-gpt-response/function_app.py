import azure.functions as func
import logging
import json
import os

from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential
from motor.motor_asyncio import AsyncIOMotorClient 

app = func.FunctionApp()
db_client = AsyncIOMotorClient(os.environ['DB_CONNECTION_URL'])
db = db_client['woosunggpt']

pubsub_client = WebPubSubServiceClient(endpoint=os.environ['PUBSUB_CONNECTION_URL'], 
                                       hub=os.environ['PUBSUB_HUB'], 
                                       credential=AzureKeyCredential(os.environ['PUBSUB_KEY']))


@app.service_bus_queue_trigger(arg_name="msg", queue_name="process-response-queue",
                               connection="SERVICEBUS_CONNECTION_URL") 
async def process_response_function(msg: func.ServiceBusMessage):
    response = json.loads(msg.get_body().decode('utf-8'))
    response['_id'] = str(response['_id'])
    await db.messages.insert_one(response)
    await pubsub_client.send_to_group(group=response['channel_id'], message=response)


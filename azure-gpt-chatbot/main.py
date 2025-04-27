from typing import Union
from fastapi import FastAPI
from dto.question import QuestionRequest
from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential


PUBSUB_ENDPOINT = ""
PUBSUB_HUB = "dev_hub"
PUBSUB_KEY = ""

app = FastAPI()
pubsub_client = WebPubSubServiceClient(endpoint=PUBSUB_ENDPOINT, hub=PUBSUB_HUB, credential=AzureKeyCredential(PUBSUB_KEY))

@app.get("/question")
async def send_question(request: QuestionRequest):
    return request

@app.get("/pubsub/token")
async def read_root(channel_id: str):
    return await pubsub_client.get_client_access_token(groups=[channel_id], minutes_to_expire=5, roles=['webpubsub.joinLeaveGroup.' + channel_id])

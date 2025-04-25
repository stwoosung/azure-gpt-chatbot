from typing import Union
from fastapi import FastAPI
from dto.question import QuestionRequest
from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential

import azure.functions as func
import os

fast_app = FastAPI()
app = func.AsgiFunctionApp(app=fast_app, http_auth_level=func.AuthLevel.ANONYMOUS)
pubsub_client = WebPubSubServiceClient(endpoint=os.environ['PUBSUB_CONNECTION_URL'], 
                                       hub=os.environ['PUBSUB_HUB'], 
                                       credential=AzureKeyCredential(os.environ['PUBSUB_KEY']))

@fast_app.get("/question")
async def send_question(request: QuestionRequest):
    return request

@fast_app.get("/pubsub/token")
async def read_root(channel_id: str):
    return await pubsub_client.get_client_access_token(groups=[channel_id], minutes_to_expire=5, roles=['webpubsub.joinLeaveGroup.' + channel_id])
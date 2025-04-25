pip install fastapi
pip install "uvicorn[standard]"
pip install azure-messaging-webpubsubservice
pip install aiohttp
pip install azure-functions

uvicorn main:app --reload

npm install -g azure-functions-core-tools


host.json에 extensions: routePreFix 추가
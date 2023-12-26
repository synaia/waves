import os
from fastapi import FastAPI, File, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import streaming.stream as stream
import modules.user_main as user_main

app = FastAPI()

base_path = os.getcwd()
key_pem = os.getcwd() + '/certs/key.pem'
public_pem = os.getcwd() + '/certs/public.crt'

app.include_router(stream.router)
app.include_router(user_main.router)

if __name__ == "__main__":
    import uvicorn

    app.mount("/test", StaticFiles(directory="./test/", html=True), name="test")
    uvicorn.run(app, host="127.0.0.1", port=8000, ssl_keyfile=key_pem, ssl_certfile=public_pem)

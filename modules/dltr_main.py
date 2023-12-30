from fastapi import APIRouter

import sys
import os
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, Security, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from dbms.database import get_db
import query.user_query as user_query
import schemas.users as schemas
import modules.user_models as models
from query.user_query import Token
from query.user_query import create_access_token, logout_token
from query.user_query import ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_SECONDS
from query.user_query import validate_permissions
from dbms.Query import Query

router = APIRouter(prefix='/dltr', tags=['dltr'])

gettrace = getattr(sys, 'gettrace', None)
# is debug mode :-) ?
if gettrace():
    path = os.getcwd() + '/dbms/query.sql'
    print('Debugging :-* ')
else:
    path = os.getcwd() + '/dbms/query.sql'
    print('Run normally.')

query = Query(path)


def dl_audio(url: str):
    from pydub import AudioSegment
    import base64
    from pytube import YouTube
    import os

    output_path = "audios"
    os.makedirs(output_path, exist_ok=True)
    pathfile = url.split("?")[1]
    pathfile = f"{output_path}/{pathfile[2:]}.mp4"

    if not os.path.exists(pathfile):
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=output_path)
        os.rename(out_file, pathfile)

    # audio = AudioSegment.from_file(pathfile, format="mp4")
    # audio_base64 = base64.b64encode(audio.export(format="wav").read())
    # return audio_base64.decode("utf-8")
    o =  f"https://127.0.0.1:8000/{pathfile}"
    return o


@router.get("/",)
async def get_audio(url: str, db: Session = Depends(get_db)):
    try:
        return dl_audio(url)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


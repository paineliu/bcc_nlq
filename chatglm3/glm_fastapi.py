
# -*- coding:utf-8 -*-
import os
import time
from typing import Union, List
from typing import Optional
import uvicorn
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from nlsql import NL2SQL

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='jss lang-elem server')
    parser.add_argument('-m', '--message', type=int, default=1, required=False, help='output debug message')
    parser.add_argument('-p', '--port', type=int, default=8102, required=False, help='port number')
    parser.add_argument('-w', '--workers', type=int, default=1, required=False, help='worker number')

    return parser.parse_args()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load resources
    global g_nl2sql
    print('liftspan', 'start...')
    args = parse_args()
    g_nl2sql = NL2SQL('./output/sql_merge')
    print('liftspan', 'finish.')
    yield
    # Clean up and release resources
    pass

app = FastAPI(lifespan=lifespan)
      
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"The parameter is incorrect. {request.method} {request.url}")
    return JSONResponse({"code": "400", "message": exc.errors()})


class Nl2SqlModel(BaseModel):
    text: str

class TokenModel(BaseModel):
    userName: str = ''

class UsageModel(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ResondData(BaseModel):
    id: str = "chatcmpl-123"
    obj: str = "chat.completion"
    created: int = 1677652288
    result: str

class RespondModel(BaseModel):
    code:int = 0
    message:str = "OK"
    data:ResondData


@app.post("/nl2sql")
async def nl2sql(charRequestModel: Nl2SqlModel):    
    print('{} {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), charRequestModel.model_dump()), end=' ')
    start = time.time()
    result = g_nl2sql.sql(charRequestModel.model_dump())
    end = time.time()
    print(end-start)
    return result

@app.post("/nl2bcc")
async def nl2bcc(charRequestModel: Nl2SqlModel):    
    print('{} {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), charRequestModel.model_dump()), end=' ')
    start = time.time()
    result = g_nl2sql.bcc(charRequestModel.model_dump())
    end = time.time()
    print(end-start)
    return result


if __name__ == "__main__":
    args = parse_args()
    print('glm_fastapi server', 'port = {}, worker = {}.'.format(args.port, args.workers))
    uvicorn.run(app='glm_fastapi:app', host='0.0.0.0', log_level='warning', port=args.port, workers=args.workers, reload=False)

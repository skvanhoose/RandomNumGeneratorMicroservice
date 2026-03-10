from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import secrets

app = FastAPI()

# to test locally, add your port to origins list. Ex: http://localhost:<PORT>
origins = ['http://localhost:4000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)


# accept only JSON strings with this structure
class NumRange(BaseModel):
    upper_limit: int | None = Field(default=None, gt=3)
    lower_limit: int | None = Field(default=None, ge=0)
    num_bytes: int | None = Field(default=None, ge=1)
    type: Literal["int", "hex", "jti"]


async def gen_int(gen_random, lower_limit, upper_limit):
    if upper_limit is None:
        if lower_limit is None:
            rand_int = gen_random.randint(0, 1000)
        else:
            rand_int = secrets.randbelow(1000)
    else:
        if lower_limit:
            print('here2')
            rand_int = gen_random.randint(lower_limit, upper_limit)
        else:
            rand_int = secrets.randbelow(upper_limit)

    return rand_int


async def gen_hex(num_bytes):
    if not num_bytes:
        num_bytes = 16
    return secrets.token_hex(num_bytes)


async def gen_token(num_bytes):
    if not num_bytes:
        num_bytes = 32
    return secrets.token_urlsafe(num_bytes)


@app.post('/num-gen')
async def gen_num(req: NumRange):
    gen_random = secrets.SystemRandom()
    num_type = req.type
    lower_limit = req.lower_limit
    upper_limit = req.upper_limit
    num_bytes = req.num_bytes

    if num_type == "int":
        try:
            rand_int = await gen_int(gen_random, lower_limit, upper_limit)
            return rand_int
        except:
            raise HTTPException(status_code=500, detail='Could not generate random int')

    elif num_type == "hex":
        try:
            rand_hex = await gen_hex(num_bytes)
            return rand_hex
        except:
            raise HTTPException(status_code=500, detail='Could not generate random hex')
    else:
        try:
            rand_token = await gen_token(num_bytes)
            return rand_token
        except:
            raise HTTPException(status_code=500, detail='Could not generate random token')
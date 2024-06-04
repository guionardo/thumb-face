import os
import tempfile

import toml
from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response

import log
from face_recognition import get_face_image, start_face_recognition

log.setup()

log.logger.info("API is starting up")

with open("pyproject.toml") as file:
    pp = toml.load(file)
    version = pp["tool"]["poetry"]["version"]
    description = pp["tool"]["poetry"]["description"]


configurations = dict(
    title="Thumb Face",
    version=version,
    description=description,
    on_startup=[start_face_recognition],
    contact=dict(
        name="Guionardo Furlan",
        url="https://github.com/guionardo",
        email="guionardo@gmail.com",
    ),
    license_info=dict(name="MIT", url="https://opensource.org/license/mit"),
)
app = FastAPI(**configurations)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthcheck")
def read_health():
    return {"status": "ok"}


@app.post(
    "/face",
    responses={200: {"content": {"image/png": {}}}},
    response_class=FileResponse,
)
async def face_thumb(image: UploadFile, size: int = 250):
    if image.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(400, "Expected image")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_image = os.path.join(tmpdir, image.filename)
        content = await image.read()
        with open(tmp_image, "wb") as file:
            file.write(content)
        face_file = get_face_image(tmp_image, size)

        with open(face_file, "br") as file:
            return Response(content=file.read(), media_type="image/png")

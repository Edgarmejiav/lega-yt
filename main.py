from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pytube import YouTube


def download_video(url, ruta_destino='./'):
    try:
        video = YouTube(url)
        stream = video.streams.get_highest_resolution()
        video_info = {
            "title": video.title,
            "author": video.author,
            "filename": stream.default_filename,
            "destination_path": ruta_destino
        }
        stream.download(output_path=ruta_destino)
        return video_info
    except Exception as e:
        return {"error": str(e)}


app = FastAPI()

origins = [
    "*",
    # "http://localhost:3000",
    # "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
some_file_path = "Houdini.mp4"


@app.get("/")
async def root():
    return "Hello, world!"


@app.get("/yt/")
async def download_and_return_video(name: str):
    video_info = download_video(name, "./")
    file_path = f"{video_info['destination_path']}{video_info['filename']}"
    return FileResponse(file_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pytube import YouTube
import os


def download_video(url, output_path='/tmp'):
    try:
        video = YouTube(url)
        stream = video.streams.get_highest_resolution()
        video_info = {
            "title": video.title,
            "author": video.author,
            "filename": stream.default_filename,
            "destination_path": output_path
        }
        stream.download(output_path=output_path)
        return video_info
    except Exception as e:
        return {"error": str(e)}


def delete_all_files(path):
    videos_deleted = []
    try:
        for file in os.listdir(path):
            if file.endswith(".mp4"):
                os.remove(os.path.join(path, file))
                videos_deleted.append(file.title())
        return videos_deleted
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


@app.get("/")
async def root():
    return "Hola este es el servidor de descarga de videos de youtube! " \
           "Para descargar un video de youtube, ingresa a la ruta /yt/?urlYt= y agrega el nombre del video despues de la barra. "
# example: http://localhost:8000/yt/?urlYt=https://www.youtube.com/watch?v=kPC_evpbwDM

@app.get("/yt/")
async def download_and_return_video(urlYt: str):
    video_info = download_video(urlYt, "/tmp")
    file_path = f"{video_info['destination_path']}{video_info['filename']}"
    return FileResponse(file_path)


@app.get("/delete_files/")
async def delete_files():
    return delete_all_files(os.getcwd())

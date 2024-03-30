from fastapi import FastAPI, File, UploadFile , Response , Form , Request  , Header
from fastapi.responses import HTMLResponse , FileResponse
from image_to_video import render_video
from fastapi.middleware.cors import CORSMiddleware
from typing import List , Annotated
import multipart
import os
import asyncio
from threading import Thread
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadfiles/")
async def create_upload_files(file: List[UploadFile] = File(...),  uid: str = Header(...)):
    print(uid)
    print(file) 
    for files in file:
        print(files.filename)
        contents = await files.read()
        if files.filename.endswith(".mp4"):
            if not os.path.exists(f"./incoming_videos/{uid}"):
                if not os.path.exists(f"./incoming_videos"):
                    os.mkdir(f"./incoming_videos")
                os.mkdir(f"./incoming_videos/{uid}")
            f = open(f"./incoming_videos/{uid}/{files.filename}", "wb+") # create a file with the name of the uploaded file
            f.write(contents)
            f.close()
        if files.filename.endswith(".mp3"):
            if not os.path.exists(f"./incoming_audio/{uid}"):
                if not os.path.exists(f"./incoming_audio"):
                    os.mkdir(f"./incoming_audio")
                os.mkdir(f"./incoming_audio/{uid}")
            f = open(f"./incoming_audio/{uid}/{files.filename}", "wb+")
            f.write(contents)
            f.close()
        if files.filename.endswith(".jpg") or files.filename.endswith(".jpeg") or files.filename.endswith(".png"):
            if not os.path.exists(f"./incoming_images/{uid}"):
                if not os.path.exists(f"./incoming_images"):
                    os.mkdir(f"./incoming_images")
                os.mkdir(f"./incoming_images/{uid}")
            f = open(f"./incoming_images/{uid}/{files.filename}", "wb+")
            f.write(contents)
            f.close()
    return {"message": "Form data"}

    # for file in files:
        
        # print(contents)
        
        # print(contents)
    # return Response(content="File uploaded")

@app.get("/get-video")
async def get_video(uid: str = Header(...)):
    # Specify the path to the video file
    def render_v(uid):
        op = render_video(uid)
        return op
    if not os.path.exists(f"./output/{uid}"):
        if not os.path.exists(f"./output"):
            os.mkdir(f"./output")
        os.mkdir(f"./output/{uid}")
    t = Thread(target=render_v, args=(uid,))
    t.start()
 
    #wait for the thread to finish
    t.join()
    op = os.path.exists(f"./output/{uid}/edit.mp4")
    if op:
        return FileResponse(f"./output/{uid}/edit.mp4" , media_type="video/mp4")
    else:
        return {"message": "Error in rendering video"}

@app.delete("/delete-files")
async def delete_files(uid: str = Header(...)):
    try:
        os.system(f"rm -rf ./incoming_videos/{uid}")
        os.system(f"rm -rf ./incoming_audio/{uid}")
        os.system(f"rm -rf ./incoming_images/{uid}")
        os.system(f"rm -rf ./output/{uid}")
        return {"message": "Files deleted successfully"}
    except:
        return {"message": "Error in deleting files"}

# Path: server.py
# Add code to run FastAPi App
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="
#
@app.get("/")
async def root():
    return {"message": "Hello World"}
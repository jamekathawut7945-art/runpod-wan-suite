from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os, shutil, tempfile

from backends.wan21_t2v import get_wan21
from backends.wan22 import i2v as wan22_i2v, animate as wan22_animate, ti2v as wan22_ti2v

app = FastAPI(title="Wan Suite on RunPod (5090)")

class T2VReq(BaseModel):
    prompt: str
    seconds: int = 4
    fps: int = 16
    size: str = "848x480"

@app.post("/t2v")
def t2v(req: T2VReq):
    out = get_wan21().generate(req.prompt, req.seconds, req.fps, req.size)
    return FileResponse(out, media_type="video/mp4", filename=os.path.basename(out))

@app.post("/i2v")
def i2v(image: UploadFile = File(...),
        seconds: int = Form(4),
        fps: int = Form(16),
        size: str = Form("1280*704"),
        offload: bool = Form(True)):
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, image.filename)
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    out = wan22_i2v(tmp_path, seconds=seconds, fps=fps, size=size, offload=offload)
    return FileResponse(out, media_type="video/mp4", filename=os.path.basename(out))

class AnimateReq(BaseModel):
    prompt: str
    seconds: int = 4
    fps: int = 16
    size: str = "1280*704"
    offload: bool = True

@app.post("/animate")
def animate(req: AnimateReq):
    out = wan22_animate(req.prompt, seconds=req.seconds, fps=req.fps, size=req.size, offload=req.offload)
    return FileResponse(out, media_type="video/mp4", filename=os.path.basename(out))

class TI2VReq(BaseModel):
    prompt: str
    size: str = "1280*704"
    offload: bool = True

@app.post("/ti2v")
def ti2v(req: TI2VReq):
    out = wan22_ti2v(req.prompt, size=req.size, offload=req.offload)
    return FileResponse(out, media_type="video/mp4", filename=os.path.basename(out))

@app.get("/healthz")
def health():
    return {"ok": True}

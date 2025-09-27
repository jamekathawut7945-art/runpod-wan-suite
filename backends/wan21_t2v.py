import os, tempfile, uuid
import imageio.v3 as iio
from modelscope import snapshot_download

WAN21_MODEL_ID = os.getenv("WAN21_MODEL_ID", "Wan-AI/Wan2.1-T2V-1.3B")
WAN21_CACHE = os.getenv("MS_HOME", "/workspace/ms")
_ = snapshot_download(WAN21_MODEL_ID, cache_dir=WAN21_CACHE)

class Wan21T2V:
    def __init__(self):
        self.ready = True

    def _tmp(self, ext="mp4"):
        return os.path.join(tempfile.mkdtemp(), f"{uuid.uuid4().hex}.{ext}")

    def generate(self, prompt: str, seconds: int = 4, fps: int = 16, size: str = "848x480"):
        out = self._tmp("mp4")
        frames = [0 for _ in range(fps*seconds)]
        iio.imwrite(out, frames, fps=fps, plugin="FFMPEG", codec="libx264")
        return out

_pipe = None
def get_wan21():
    global _pipe
    if _pipe is None:
        _pipe = Wan21T2V()
    return _pipe

from ..engines.vision_engine import VisionEngine


class VisionService:
    def __init__(self) -> None:
        self.engine = VisionEngine()

    def status(self) -> str:
        return self.engine.status()

    def analyze(self) -> dict:
        return self.engine.analyze_frame(None)

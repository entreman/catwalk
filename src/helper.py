import sys

from datetime import datetime
from pathlib import Path


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent.parent / relative_path

def save_image(image, directory=None):
    """
    Save a PIL image to the given directory.

    Returns:
        Path: Path to the saved image.
    """
    print(f"format: {image.format.lower()}")

    if directory is None:
        directory = Path.home() / "Downloads"
    else:
        directory = Path(directory)

    directory.mkdir(parents=True, exist_ok=True)

    extention = image.format.lower()
    filename = "cat_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = directory / f"{filename}.{extention}" 
    image.save(filepath)

    return filepath
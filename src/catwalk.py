#!/usr/bin/env python3

import argparse
import io
import queue
import threading
import time
import requests
import tkinter as tk
import sys

from PIL import Image, ImageTk
from pathlib import Path

from slideshowcontroller import SlideshowController
from catwalkapp import CatwalkApp
   

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "delay",
        nargs="?",
        type=int,
        default=3,
        help="seconds between downloads"
    )
    args = parser.parse_args()


    app = CatwalkApp(delay=args.delay)
    app.run()
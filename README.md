# videoanalytics

This project is about videosources emergency detection made with ZeroMQ infrastructure

## Used technologies
- ZeroMQ
- YOLOv8
- PSNR
- OpenCV
- Multiprocessing & Threading

## Prerequisites

- Torch with CUDA
- Python3.12

## Usage

- `pip install -r requirements.txt`
- Download all necessary files from [Google Drive](https://drive.google.com/drive/u/0/folders/1OI_XtRNcwbm-JvojeKGR_x1SE1GuonQq) :
 - (optional) place test videos & meanframes to `./videos` folder
 - place YOLO models to `./models` folder
- set up `config.json` with actual files locations, ip addresses & ports, psnr threshold

Notes:
> meanframes must have same resolution as original videos, '.jpg' hardcoded <BR>
> meanframes were created on "normal" parts of videos with `psnr.py`

Usage (`Ctrl+C` to stop):
```bash
python run.py
```

## TODOs
- create meanframes automatically
- train models on another datasets
- add resolution to config
- Ctrl+C handler
- Auto scale processes
- Test on realtime videosources
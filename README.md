# object-detection-format-converter

Dataset format converter for object detection

## Overview
Deep learning field for image processing has many dataset format. For object detection task, MSCOCO, Yolo, PascalVOC and so on are frequently used and sometimes we have to convert our dataset annotation files to another. To deal with this, I creat dataset format converter for object detection. Supported dataset formats are below.

[x] MSCOCO  
[x] Yolo  
[x] PascalVOC  
[x] KITTI

## Prerequisites
* Python >= 3.7
* numpy
* opencv

Install python>=3.7 and run commands below.
```bash
pip install -U pip
pip install opencv-python
```

## Usage
Call '[convert_format](./utils/convert.py)' function with some args.
### Example
```python
from utils.convert import convert_format

convert_format(
    src_format="coco",
    dst_format="yolo",
    src_path="./coco.json",
    dst_path="./yolo_output",
    class_txt_path="",
)
```
Sample code is available [here](./sample.py). Detail descriptions are [here](#description-of-each-data-format)

If args of 'class_txt_path' is empty, scan all annotation files and create class list automaticaly(alphabetical order).

## Detail Description 
### Description of Each Data Format
* [MSCOCO](./docs/README_mscoco.md)
* [YOLO](./docs/README_yolo.md)
* [PascalVOC](./docs/README_pascalvoc.md)
* [KITTI](./docs/README_kitti.md)

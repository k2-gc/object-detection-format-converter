# object-detection-format-converter

Dataset format converter for object detection

## Overview
Deep learning field for image processing has many dataset format. For object detection task, MSCOCO, YOLO, PascalVOC and so on are frequently used and sometimes we have to convert our dataset annotation files to another. To deal with this, I creat dataset format converter for object detection. Supported dataset formats are below.

* [x] MSCOCO  
* [x] YOLO
* [x] PascalVOC  
* [x] KITTI

## Prerequisites
* Python >= 3.8

## Installation
Install python>=3.8 and run commands below in your venv or something.
```bash
pip install -U pip setuptools build
python -m build
pip install dist/objdet_converter-1.2.0-py3-none-any.whl
```

## Usage
### CLI
```bash
objdet-conv convert --src-format 'SRC_FORMAT' --dst-format 'DST_FORMAT' --src-path 'PATH_TO_SRC' --dst-path 'PAST_TO_OUTPUT' --class-txt-path 'IF NEEDED'
```
Supported format strings:
1. coco
2. yolo
3. pascalvoc
4. kitti
#### Example
```bash
objdet-conv convert --src-format yolo --dst-format coco --src-path ./yolo_dir --dst-path ./output --class-txt-path ./yolo_dir/classes.txt
```
### Call from Function
Call '[convert_format](./objdet_converter/utils/convert.py)' function with some args.
####  Example
```python
from objdet_converter.convert import convert_format

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
* [Custom Dataset Implementation](./docs/README_custom.md)

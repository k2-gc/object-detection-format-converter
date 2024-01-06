# MSCOCO
| Item | Description |
| :-: | :- |
| Format name | "coco" |
| Input file/dir | JSON file path |
| Output file/dir | Directory path or JSON file path <br /> If directory path, 'dir-path'/annotation.json will be created|
| Image input | Not Required |


## Example
### From MSCOCO
#### Code Example
```python
from objdet_converter.utils.convert import convert_format

convert_format(
    src_format="coco",
    dst_format=CONVERT_OUTPUT_FORMAT,
    src_path="./dir/coco.json",
    dst_path=OUTPUT_DIR,
    class_txt_path="",
)
```
#### Input File Structure Example
```
./dir/
  └─ coco.json
```
### To MSCOCO
#### Code Example
```python
from objdet_converter.utils.convert import convert_format

convert_format(
    src_format=CONVERT_INPUT_FORMAT,
    dst_format="coco",
    src_path=INPUT_DIR,
    dst_path="./coco_output",
    class_txt_path="",
)
```
or 
```python
from objdet_converter.utils.convert import convert_format

convert_format(
    src_format=CONVERT_INPUT_FORMAT,
    dst_format="coco",
    src_path=INPUT_DIR,
    dst_path="./coco_output/output.json",
    class_txt_path="",
)
```
The first case, "./coco_output/annotation.json" will be created as a result file.

#### Output File Structure Example
```
./coco_output/
  └─ annotation.json
```
or 
```
./coco_output/
  └─ output.json
```
## Converted Output Example
```json
{
    "info": {
        "description": "Custom Dataset",
        "url": "",
        "version": "",
        "year": "",
        "contributor": "",
        "date_created": ""
    },
    "licenses": [
        {
            "url": "Unspecified",
            "id": 100,
            "name": "Unspecified"
        }
    ],
    "images": [
        {
            "license": 100,
            "file_name": "000000037777.jpg",
            "coco_url": ABSOLUTE PATH to IMAGE,
            "height": 230,
            "width": 352,
            "date_captured": CREATED TIME,
            "flickr_url": "",
            "id": 0
        },
        ...
    ],
    "annotations": [
        {
            "segmentation": [],
            "num_keypoints": 0,
            "area": 136,
            "iscrowd": 0,
            "keypoints": [],
            "image_id": 0,
            "bbox": [
                102,
                118,
                8,
                17
            ],
            "category_id": 64,
            "id": 1,
            "caption": "hoge hoge",
            // If converting from KITTI with score
            "score": 0.8
        },
        ...
    ],
    "categories": [
        {
            "supercategory": "Unspecified",
            "id": 1,
            "name": "person",
            "keypoints": [],
            "skeleton": []
        },
        ...
    ]
}
```
If converting from kitti with score to mscoco, "score" key and value will be added. In other case, "score" key and value will not be appeared.
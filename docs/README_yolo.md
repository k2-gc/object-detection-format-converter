# YOLO
| Item | Description |
| :-: | :- |
| Format name | "yolo" |
| Input file/dir | Directory path that contains **image files** and **annotation files** |
| Output file/dir | Directory path |
| Image Input | Required (Locate in input directory with annotation files) |


## Example
### From YOLO
#### Code Example
```python
from objdet_converter.utils.convert import convert_format

convert_format(
    src_format="yolo",
    dst_format=CONVERT_OUTPUT_FORMAT,
    src_path="./dir/",
    dst_path=OUTPUT_DIR,
    class_txt_path="",
)
```
#### Input File Structure Example
```
./dir/
  ├─ image_00000.png
  ├─ image_00000.txt
  ├─ image_00001.png
  ├─ image_00001.txt
  ├─ image_00002.png
  └─ image_00002.txt
```
### To YOLO
#### Code Example
```python
from objdet_converter.utils.convert import convert_format

convert_format(
    src_format=CONVERT_INPUT_FORMAT,
    dst_format="yolo",
    src_path=INPUT_DIR,
    dst_path="./yolo_output",
    class_txt_path="",
)
```


#### Output File Structure Example
```
./yolo_output/
  ├─ image_00000.txt
  ├─ image_00001.txt
  ├─ image_00002.txt
  ├─ ...
  └─ classes.txt
```


## Converted Output Example
### Annotation File
```txt
63 0.3011 0.55 0.0227 0.0739
61 0.1619 0.9652 0.1761 0.0609
61 0.4006 0.8783 0.142 0.113
...
```
### Classes.txt
```txt
person
bicycle
car
...
```

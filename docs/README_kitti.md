# KITTI
| Item | Description |
| :-: | :- |
| Format name | "kitti" |
| Input file/dir | Directory path that contains **image files** and **annotation files** |
| Output file/dir | Directory path |
| Image Input | Required (Locate in input directory with corresponding annotation files) |

## Example
### From KITTI
#### Code Example
```python
from objdet_converter.utils.convert import convert_format

convert_format(
    src_format="kitti",
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
### To KITTI
#### Code Example
```python
from objdet_converter.utils.convert import convert_format

convert_format(
    src_format=CONVERT_INPUT_FORMAT,
    dst_format="kitti",
    src_path=INPUT_DIR,
    dst_path="./kitti_output",
    class_txt_path="",
)
```


#### Output File Structure Example
```
./kitti_output/
  ├─ image_00000.txt
  ├─ image_00001.txt
  └─ image_00002.txt
```
## Converted Output Example
### Without score
```txt
potted-plant 0.0 0 0 102 118 110 135 0 0 0 0 0 0 0
chair 0.0 0 0 26 215 88 229 0 0 0 0 0 0 0
chair 0.0 0 0 116 189 166 215 0 0 0 0 0 0 0
dining-table 0.0 0 0 79 178 287 226 0 0 0 0 0 0 0
...
```
### With score(Only converting from mscoco with score)
```txt
potted-plant 0.0 0 0 102 118 110 135 0 0 0 0 0 0 0 0.9
chair 0.0 0 0 26 215 88 229 0 0 0 0 0 0 0 0.8
chair 0.0 0 0 116 189 166 215 0 0 0 0 0 0 0 0.5
dining-table 0.0 0 0 79 178 287 226 0 0 0 0 0 0 0 0.7
...
```
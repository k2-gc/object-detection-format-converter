# PascalVOC
| Item | Description |
| :-: | :- |
| Format name | "pascalvoc" |
| Input file/dir | Directory path that contains **XML annotation files** |
| Output file/dir | Directory path |
| Image Input | Not Required in case that 'size' info is provided in XML file |

# Example
### From PascalVOC
#### Code Example
```python
from objdet_converter.convert import convert_format

convert_format(
    src_format="pascalvoc",
    dst_format=CONVERT_OUTPUT_FORMAT,
    src_path="./dir/",
    dst_path=OUTPUT_DIR,
    class_txt_path="",
)
```
#### Input File Structure Example
```
./dir/
  ├─ image_00000.xml
  ├─ image_00001.xml
  └─ image_00002.xml
```
or
```
./dir/
  ├─ image_00000.png
  ├─ image_00000.xml
  ├─ image_00001.png
  ├─ image_00001.xml
  ├─ image_00002.png
  └─ image_00002.xml
```
If image width and image height information are provided in xml file, image files are not required.

### To PascalVOC
#### Code Example
```python
from objdet_converter.convert import convert_format

convert_format(
    src_format=CONVERT_INPUT_FORMAT,
    dst_format="pascalvoc",
    src_path=INPUT_DIR,
    dst_path="./pascalvoc_output",
    class_txt_path="",
)
```


#### Output File Structure Example
```
./pascalvoc_output/
  ├─ image_00000.xml
  ├─ image_00001.xml
  └─ image_00002.xml
```


## Converted Output Example
```xml
<annotation>
  <folder>PARENT DIR NAME</folder>
  <filename>000000037777.jpg</filename>
  <path>ABSOLUTE PATH to IMAGE</path>
  <source>
    <database>Unknown</database>
  </source>
  <size>
    <width>352</width>
    <height>230</height>
    <depth>3</depth>
  </size>
  <segmented>1</segmented>
  <object>
    <name>potted-plant</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <bndbox>
      <xmin>102</xmin>
      <ymin>118</ymin>
      <xmax>110</xmax>
      <ymax>135</ymax>
    </bndbox>
  </object>
  <object>
    <name>orange</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <bndbox>
      <xmin>217</xmin>
      <ymin>200</ymin>
      <xmax>232</xmax>
      <ymax>214</ymax>
    </bndbox>
  </object>
  ...
</annotation>
```

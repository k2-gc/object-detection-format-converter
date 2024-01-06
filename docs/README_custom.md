# Custom Dataset
## How to Implement Your Own Datset Converter

### Create Your Dataset Class
1. Inherit [BaseDataFormat](../objdet_converter/utils/base.py) class
2. Implement some functions.
* \_\_init\_\_()  
Call **_parse_annotation()** and **_parse_class_list()**  
Create **MSCOCODataset()** instance.
* _parse_annotation()  
Implement annotation parser and set **self.image_id_to_image_info** and **self.image_id_to_annotation_list**.
```python
self.image_id_to_image_info[IMAGE_ID] = {
  "file_name": IMAGE_FILE_NAME,
  "file_path": IMAGE_FILE_PATH,
  "width": IMAGE_WIDTH,
  "height": IMAGE_HEIGHT,
}
```
```python
self.image_id_to_annotation_list[IMAGE_ID].append({
    "annotation_id": ANNOTATION_ID,
    "class_id": CLASS_ID,
    "bbox": BBOX, # Absolute points [left, top, width, height]
    "score": SCORE or None, # If exists, otherwise None
})
```

* _parse_class_list()  
Implement class list parser and set **self.class_id_to_class_name** and **self.class_name_to_class_id**.
* convert()  
Refer to [YOLO class](../objdet_converter/utils/yolo.py)
* validation_check()  
Refer to [YOLO class](../objdet_converter/utils/yolo.py)

3. Add Supporting Dataset Format
Add your own dataset format name to the programs.
* [supported_data_format_list](../objdet_converter/utils/utils.py)
* [create_src_dataset_class()](../objdet_converter/utils/format_converter.py)
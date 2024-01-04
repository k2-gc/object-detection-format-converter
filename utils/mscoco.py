from collections import defaultdict
import datetime
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import cv2
import numpy as np

from utils.base import BaseDataFormat
from utils.utils import absolute2relative, calculate_area, get_rectangle_all_points, topleftwh2centerwh, topleftwh2topleftbottomright

class MSCOCODataset(BaseDataFormat):
    """Dataset parser for MSCOCO
       This class mainly takes charge of converting.
       See 'base.py' as well.
    """
    def __init__(self, dst_path, class_txt_path, src_path="") -> None:
        super().__init__(dst_path, class_txt_path, src_path)
        
        self.info_dict = {
            "info": {
                "description": "Custom Dataset",
                "url": "",
                "version": "",
                "year": "",
                "contributor": "",
                "date_created": ""
            }
        }
        self.license = {
            "licenses": [
	            {
		            "url": "Unspecified",
                    "id": 100,
                    "name": "Unspecified"
	            },
            ]
        }
        if str(self.src_path) != ".":
            self._parse_annotation()
            self._parse_class_list()

    
    def _parse_class_list(self):
        def fullfill_lacked_id(category_id_to_name):
            i = min(category_id_to_name)
            tmp = dict()
            for category_id, category_name in category_id_to_name.items():
                if not i == category_id:
                    while True:
                        tmp[i] = i
                        i += 1
                        if i == category_id:
                            break
                tmp[category_id] = category_name
                i = category_id + 1
            return tmp
        with open(self.src_path) as f:
            json_content = json.load(f)
        assert "categories" in json_content, "Class information not provided. 'Categories' key not found."
        # TODO:
        # If classes.txt is provided, create categories from the file.
        category_list = json_content["categories"]
        tmp = dict()
        for category in category_list:
            class_id = category["id"]
            class_name = category["name"]
            tmp[class_id] = class_name
        id_sorted_list = sorted(tmp.items(), key=lambda x:x[0])
        # If not sequential id, index no. is used to fullfille lacked class id alternatively.
        # id_sorted_list = fullfill_lacked_id(id_sorted_list)
        class_id_to_class_name = {class_id: class_name for class_id, class_name in id_sorted_list}
        self.class_id_to_class_name = fullfill_lacked_id(class_id_to_class_name)
        self.class_name_to_class_id = {self.class_id_to_class_name[class_id]: idx+1 for idx, class_id, in enumerate(self.class_id_to_class_name)}

    def _parse_annotation(self):
        with open(self.src_path) as f:
            json_content = json.load(f)
        assert "images" in json_content, f"'images' key is not appeared in {self.src_path}"
        assert "annotations" in json_content, f"'annotations' key is not appeared in {self.src_path}"
        image_info_list = json_content["images"]
        annotation_list = json_content["annotations"]
        for image_info in image_info_list:
            image_id = image_info["id"]
            file_name = image_info["file_name"]
            file_path = image_info["file_name"]
            width = image_info["width"]
            height = image_info["height"]
            self.image_id_to_image_info[image_id] = {
                "file_name": file_name,
                "file_path": file_path,
                "width": width,
                "height": height,
            }
        for annotation in annotation_list:
            annotation_id = annotation["id"]
            class_id = annotation["category_id"]
            image_id = annotation["image_id"]
            bbox = annotation["bbox"]
            score = None
            if "score" in annotation:
                score = annotation["score"]
            self.image_id_to_annotation_list[image_id].append({
                "annotation_id": annotation_id,
                "class_id": class_id,
                "bbox": bbox,
                "score": score,
            })

    def _convert_to_yolo(self):
        self.dst_path.mkdir(exist_ok=True, parents=True)
        for image_id, image_info in self.image_id_to_image_info.items():
            image_name = image_info["file_name"]
            annotation_path = self.dst_path / Path(image_name).with_suffix(".txt")
            image_width = image_info["width"]
            image_height = image_info["height"]
            annotation_list = self.image_id_to_annotation_list[image_id]
            with open(annotation_path, "w") as f:
                for annotation in annotation_list:
                    # MSCOCO "categories" in json file is not sequential
                    original_class_id = annotation["class_id"]
                    class_name = self.class_id_to_class_name[original_class_id]
                    class_id = self.class_name_to_class_id[class_name]
                    bbox = annotation["bbox"]
                    bbox = topleftwh2centerwh(bbox)
                    bbox = absolute2relative(bbox, image_width, image_height)
                    bbox = [np.clip(b, 0, 1) for b in bbox]
                    bbox = [str(round(b, 4)) for b in bbox]
                    print(f"{class_id-1} {' '.join(bbox)}", file=f)
        with open(self.dst_path / "classes.txt", "w") as f:
            for _, class_name in self.class_id_to_class_name.items():
                print(class_name, file=f)

    def _convert_to_kitti(self):
        self.dst_path.mkdir(exist_ok=True, parents=True)
        for image_id, image_info in self.image_id_to_image_info.items():
            image_name = image_info["file_name"]
            annotation_path = self.dst_path / Path(image_name).with_suffix(".txt")
            image_width = image_info["width"]
            image_height = image_info["height"]
            annotation_list = self.image_id_to_annotation_list[image_id]
            with open(annotation_path, "w") as f:
                for annotation in annotation_list:
                    # Original MSCOCO "categories" in json file is not sequential
                    original_class_id = annotation["class_id"]
                    class_name = self.class_id_to_class_name[original_class_id]
                    # In case that class name includes space
                    class_name = class_name.replace(' ', '-')
                    bbox = annotation["bbox"]
                    bbox = topleftwh2topleftbottomright(bbox)
                    bbox[0] = np.clip(bbox[0], 0, image_width)
                    bbox[1] = np.clip(bbox[1], 0, image_height)
                    bbox[2] = np.clip(bbox[2], 0, image_width)
                    bbox[3] = np.clip(bbox[3], 0, image_height)
                    bbox = [str(round(b, 4)) for b in bbox]
                    truncated = 0.0
                    occluded = 0
                    alpha = 0
                    dimensions = [str(0) for _ in range(3)]
                    location = [str(0) for _ in range(3)]
                    rotation_y = 0
                    score = annotation["score"]
                    if score:
                        print(f"{class_name} {truncated} {occluded} {alpha} {' '.join(bbox)} {' '.join(dimensions)} {' '.join(location)} {rotation_y} {score}", file=f)
                    else:
                        print(f"{class_name} {truncated} {occluded} {alpha} {' '.join(bbox)} {' '.join(dimensions)} {' '.join(location)} {rotation_y}", file=f)

    def _convert_to_pascalVOC(self):
        self.dst_path.mkdir(exist_ok=True, parents=True)
        for image_id, image_info in self.image_id_to_image_info.items():
            image_name = image_info["file_name"]
            image_path = image_info["file_path"]
            annotation_path = self.dst_path / Path(image_name).with_suffix(".xml")
            image_width = image_info["width"]
            image_height = image_info["height"]
            image_channel = 3
            if Path(image_path).exists():
                image = cv2.imread(image_path)
                image_channel = image.shape[-1]
            root = ET.Element('annotation')
            folder_elem = ET.SubElement(root, 'folder')
            filename_elem = ET.SubElement(root, 'filename')
            path_elem = ET.SubElement(root, 'path')
            source_elem = ET.SubElement(root, 'source')
            size_elem = ET.SubElement(root, 'size')
            segmented_elem = ET.SubElement(root, 'segmented')
            folder_elem.text = "Unknown"
            if len(Path(image_path).parts) > 1:
                folder_elem.text = str(Path(image_path).parents[-2])
            filename_elem.text = image_name
            path_elem.text = image_path
            ET.SubElement(source_elem, "database").text = "Unknown"
            ET.SubElement(size_elem, "width").text = str(image_width)
            ET.SubElement(size_elem, "height").text = str(image_height)
            ET.SubElement(size_elem, "depth").text = str(image_channel)
            segmented_elem.text = "1"
            
            annotation_list = self.image_id_to_annotation_list[image_id]
            for annotation in annotation_list:
                # MSCOCO "categories" in json file is not sequential
                original_class_id = annotation["class_id"]
                class_name = self.class_id_to_class_name[original_class_id]
                bbox = annotation["bbox"]
                bbox = topleftwh2topleftbottomright(bbox)
                bbox[0] = np.clip(bbox[0], 0, image_width)
                bbox[1] = np.clip(bbox[1], 0, image_height)
                bbox[2] = np.clip(bbox[2], 0, image_width)
                bbox[3] = np.clip(bbox[3], 0, image_height)
                bbox = [str(int(b)) for b in bbox]
                object_elem = ET.SubElement(root, "object")
                ET.SubElement(object_elem, "name").text = class_name
                ET.SubElement(object_elem, "pose").text = "Unspecified"
                ET.SubElement(object_elem, "truncated").text = "0"
                ET.SubElement(object_elem, "difficult").text = "0"
                bbox_elem = ET.SubElement(object_elem, "bndbox")
                ET.SubElement(bbox_elem, "xmin").text = bbox[0]
                ET.SubElement(bbox_elem, "ymin").text = bbox[1]
                ET.SubElement(bbox_elem, "xmax").text = bbox[2]
                ET.SubElement(bbox_elem, "ymax").text = bbox[3]
            # doc = minidom.parseString(ET.tostring(root, 'utf-8'))
            # with open(annotation_path,'w') as f:
            #     doc.writexml(f, encoding='utf-8', newl='\n', indent='', addindent='  ')
            tree = ET.ElementTree(root)
            ET.indent(tree, space='  ')
            tree.write(str(annotation_path), xml_declaration=False)
        
    def dump_json(self):
        current_time = datetime.datetime.now()
        current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        image_info_list = defaultdict(list)
        annotation_info_list = defaultdict(list)
        category_info_list = defaultdict(list)
        for image_id, image_info in self.image_id_to_image_info.items():
            appending_image_info_dict = {
                "license": 100,
                "file_name": image_info["file_name"],
                "coco_url": image_info["file_path"],
                "height": image_info["height"],
                "width": image_info["width"],
                "date_captured": current_time,
                "flickr_url": "",
                "id": image_id
            }
            image_info_list["images"].append(appending_image_info_dict)
        for image_id, annotation_list in self.image_id_to_annotation_list.items():
            for annotation in annotation_list:
                bbox = annotation["bbox"]
                score = annotation["score"]
                appending_annotation_info_dict = {
                    # "segmentation": get_rectangle_all_points(bbox),
                    "segmentation": [],
                    "num_keypoints": 0,
                    "area": calculate_area(bbox),
                    "iscrowd": 0,
                    "keypoints": [],
                    "image_id": image_id,
                    "bbox": bbox,
                    "category_id": annotation["class_id"],
                    "id": annotation["annotation_id"],
                    "caption": "hoge hoge"
                }
                if score:
                    appending_annotation_info_dict["score"] = score
                annotation_info_list["annotations"].append(appending_annotation_info_dict)
        for category_id, category_name in self.class_id_to_class_name.items():
            category_dict = {
                "supercategory": "Unspecified",
                "id": category_id,
                "name": category_name,
                "keypoints": [],
                "skeleton": [],
            }
            category_info_list["categories"].append(category_dict)
        annotation_dict = dict()
        annotation_dict.update(self.info_dict)
        annotation_dict.update(self.license)
        annotation_dict.update(image_info_list)
        annotation_dict.update(annotation_info_list)
        annotation_dict.update(category_info_list)
        if self.dst_path.suffix != ".json":
            self.dst_path = self.dst_path / "annotation.json"
        self.dst_path.parent.mkdir(exist_ok=True, parents=True)
        with open(self.dst_path, "w") as f:
            json.dump(annotation_dict, f, indent=4)

    def convert(self, format):
        if format == "yolo":
            self._convert_to_yolo()
            return
        elif format == "kitti":
            self._convert_to_kitti()
            return
        elif format == "pascalvoc":
            self._convert_to_pascalVOC()
            return
        elif format == "coco":
            self.dump_json()
            return

    def validation_check(self):
        # assert self.src_path.exists(), f"File/Dir path '{self.src_path}' not found"
        if str(self.src_path) == ".":
            return
        assert self.src_path.suffix == ".json", f"When using mscoco, '{self.src_path}' must be json file"
        assert self.src_path.exists(), f"Annotation file '{self.src_path}' not found"

    def set_data(self, 
                 image_id_to_image_info,
                 image_id_to_annotation_list,
                 class_id_to_class_name,
                 class_name_to_class_id,
                 ):
        self.image_id_to_image_info = image_id_to_image_info
        self.image_id_to_annotation_list = image_id_to_annotation_list
        self.class_id_to_class_name = class_id_to_class_name
        self.class_name_to_class_id = class_name_to_class_id
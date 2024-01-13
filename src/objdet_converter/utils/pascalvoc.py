from pathlib import Path
import xml.etree.ElementTree as ET

import cv2

from .base import BaseDataFormat
from .mscoco import MSCOCODataset
from .utils import check_image_existence, topleftbottomright2topleftwh

class PascalVOCDataset(BaseDataFormat):
    """Dataset parser for PascalVOC
       See 'base.py' as well.
    """
    def __init__(self, dst_path, class_txt_path, src_path) -> None:
        super().__init__(dst_path, class_txt_path, src_path)
        self._parse_class_list()
        self._parse_annotation()
        self.mscooc_data = MSCOCODataset(dst_path, class_txt_path, "")
        self.mscooc_data.set_data(
            self.image_id_to_image_info,
            self.image_id_to_annotation_list,
            self.class_id_to_class_name,
            self.class_name_to_class_id
        )

    def _parse_class_list(self):
        def scan_annotation_file():
            annotation_path_list = sorted(self.src_path.glob("**/*xml"))
            tmp_class_name_list = list()
            for annotation_path in annotation_path_list:
                tree = ET.parse(annotation_path)
                root = tree.getroot()
                for obj in root.iter("object"):
                    class_name_info = obj.find("name")
                    if class_name_info is None:
                        continue
                    class_name = class_name_info.text
                    tmp_class_name_list.append(class_name)
            class_name_to_id = {class_name: index+1 for index, class_name in enumerate(sorted(set(tmp_class_name_list)))}
            id_to_class_name = {index: class_name for class_name, index in class_name_to_id.items()}
            return class_name_to_id, id_to_class_name
        if str(self.class_txt_path) == ".":
            self.class_name_to_class_id, self.class_id_to_class_name = scan_annotation_file()
            return
        if not self.class_txt_path.exists():
            self.class_name_to_class_id, self.class_id_to_class_name = scan_annotation_file()
            return
        with open(self.class_txt_path) as f:
            lines = f.read().split('\n')
        # For MSCOCO, 1-origin
        self.class_id_to_class_name = {index+1: line for index, line in enumerate(lines) if line != ""}
        self.class_name_to_class_id = {class_name: class_id for class_id, class_name in self.class_id_to_class_name.items()}

    
    def _parse_annotation(self):
        annotation_path_list = sorted(self.src_path.glob("**/*xml"))
        annotation_id = 1
        for index, annotation_path in enumerate(annotation_path_list):
            tree = ET.parse(annotation_path)
            root = tree.getroot()

            file_name = root.find("filename")
            if not file_name is None:
                image_path = Path(file_name.text)
            else:
                image_path = Path(annotation_path.stem)
                image_extension = check_image_existence(annotation_path)
                if image_extension:
                    image_path = annotation_path.with_suffix(image_extension)
            
            image_info = root.find("size")
            image_width = None
            image_height = None
            if image_info:
                width_info = image_info.find("width")
                height_info = image_info.find("height")
                if not width_info is None:
                    image_width = int(width_info.text)
                if not width_info is None:
                    image_height = int(height_info.text)
            if image_width is None:
                if image_path.exists():
                    image = cv2.imread(str(image_path))
                    image_height, image_width = image.shape[:2]
            if image_height is None:
                if image_path.exists():
                    image = cv2.imread(str(image_path))
                    image_height, image_width = image.shape[:2]
            if (image_width is None) or (image_height is None):
                print(f"Image size not specified in {annotation_path}, Ignored")
                continue
            self.image_id_to_image_info[index] = {
                "file_name": image_path.name,
                "file_path": str(image_path),
                "width": image_width,
                "height": image_height,
            }
            for i, obj in enumerate(root.iter("object")):
                class_name_info = obj.find("name")
                bbox_info = obj.find("bndbox")
                if class_name_info is None:
                    print(f"Class name not found in '{annotation_path}' {i}-th object")
                    continue
                if bbox_info is None:
                    print(f"Bbox info not found in '{annotation_path}' {i}-th object")
                    continue
                class_name = class_name_info.text
                xmin_info = bbox_info.find("xmin")
                ymin_info = bbox_info.find("ymin")
                xmax_info = bbox_info.find("xmax")
                ymax_info = bbox_info.find("ymax")
                if xmin_info is None:
                    print(f"Tag xmin not found in '{annotation_path} {i}-th object")
                    continue
                if ymin_info is None:
                    print(f"Tag ymin not found in '{annotation_path} {i}-th object")
                    continue
                if xmax_info is None:
                    print(f"Tag xmax not found in '{annotation_path} {i}-th object")
                    continue
                if ymax_info is None:
                    print(f"Tag ymax not found in '{annotation_path} {i}-th object")
                    continue
                xmin = int(xmin_info.text)
                ymin = int(ymin_info.text)
                xmax = int(xmax_info.text)
                ymax = int(ymax_info.text)
                bbox = [xmin, ymin, xmax, ymax]
                class_id = self.class_name_to_class_id[class_name]
                bbox = topleftbottomright2topleftwh(bbox)
                self.image_id_to_annotation_list[index].append({
                    "annotation_id": annotation_id,
                    "class_id": class_id,
                    "bbox": bbox,
                    "score": None,
                })
                annotation_id += 1

    def convert(self, dst_format):
        self.mscooc_data.convert(dst_format)

    def validation_check(self):
        assert self.src_path.exists(), f"Annotation directory '{self.src_path}' not found"
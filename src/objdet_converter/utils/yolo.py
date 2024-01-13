import cv2

from .base import BaseDataFormat
from .mscoco import MSCOCODataset
from .utils import check_image_existence, relative2absolute, centerwh2topleftwh

class YoloDataset(BaseDataFormat):
    """Dataset parser for Yolo
       See 'base.py' as well.
    """
    def __init__(self, dst_path, class_txt_path, src_path) -> None:
        super().__init__(dst_path, class_txt_path, src_path)
        self._create_class_dict()
        self._parse_annotation()
        self.mscooc_data = MSCOCODataset(dst_path, class_txt_path, "")
        self.mscooc_data.set_data(
            self.image_id_to_image_info,
            self.image_id_to_annotation_list,
            self.class_id_to_class_name,
            self.class_name_to_class_id
        )

    def _create_class_dict(self):
        if str(self.class_txt_path) == ".":
            # Create later
            return
        if not self.class_txt_path.exists():
            # Create later
            return
        with open(self.class_txt_path) as f:
            lines = f.read().split('\n')
        # For MSCOCO, 1-origin
        self.class_id_to_class_name = {index+1: line for index, line in enumerate(lines) if line != ""}
        self.class_name_to_class_id = {class_name: class_id for class_id, class_name in self.class_id_to_class_name.items()}

    
    def _parse_annotation(self):
        annotation_path_list = sorted(self.src_path.glob("**/*txt"))
        annotation_id = 1
        tmp_class_list = list()
        for index, annotation_path in enumerate(annotation_path_list):
            if "classes.txt" in str(annotation_path):
                continue
            image_extension = check_image_existence(annotation_path)
            if not image_extension:
                print(f"Image file corresponding to '{annotation_path}' not found")
                continue
            image_path = annotation_path.with_suffix(image_extension)
            image = cv2.imread(str(image_path))
            image_height, image_width = image.shape[:2]
            self.image_id_to_image_info[index] = {
                "file_name": image_path.name,
                "file_path": str(image_path),
                "width": image_width,
                "height": image_height,
            }
            with open(annotation_path) as f:
                lines = f.read().split('\n')
            for line in lines:
                if line == "":
                    continue
                split_line = line.split(" ")
                class_id = int(split_line[0])
                tmp_class_list.append(class_id)
                bbox = [float(b) for b in split_line[1:]]
                bbox = relative2absolute(bbox, image_width, image_height)
                bbox = centerwh2topleftwh(bbox)
                self.image_id_to_annotation_list[index].append({
                    "annotation_id": annotation_id,
                    "class_id": class_id+1,
                    "bbox": bbox,
                    "score": None,
                })
                annotation_id += 1
        if len(self.class_id_to_class_name) == 0:
            max_class_id = max(tmp_class_list)
            self.class_id_to_class_name = {class_id+1: str(class_id) for class_id in range(max_class_id+1)}
            self.class_name_to_class_id = {class_name: class_id for class_id, class_name in self.class_id_to_class_name.items()}

    def convert(self, dst_format):
        self.mscooc_data.convert(dst_format)

    def validation_check(self):
        assert self.src_path.exists(), f"Annotation directory '{self.src_path}' not found"
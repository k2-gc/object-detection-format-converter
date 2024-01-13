import cv2

from .base import BaseDataFormat
from .mscoco import MSCOCODataset
from .utils import check_image_existence, topleftbottomright2topleftwh

class KITTIDataset(BaseDataFormat):
    """Dataset parser for KITTI
       See 'base.py' as well.
    """
    def __init__(self, dst_path, class_txt_path, src_path) -> None:
        super().__init__(dst_path, class_txt_path, src_path)
        self._parse_class_list()
        self.mscoco_data = MSCOCODataset(dst_path, class_txt_path, "")
        self._parse_annotation()
        self.mscoco_data.set_data(
            self.image_id_to_image_info,
            self.image_id_to_annotation_list,
            self.class_id_to_class_name,
            self.class_name_to_class_id
        )

    def _parse_class_list(self):
        def _scan_annotation_file():
            annotation_path_list = sorted(self.src_path.glob("**/*txt"))
            appeared_class_name_list = list()
            for annotation_path in annotation_path_list:
                with open(annotation_path) as f:
                    lines = f.read().split('\n')
                for line in lines:
                    if line == "":
                        continue
                    split_line = line.split(" ")
                    class_name = split_line[0]
                    appeared_class_name_list.append(class_name)
            unique_class_list = sorted(list(set(appeared_class_name_list)))
            class_id_to_class_name = {index+1: line for index, line in enumerate(unique_class_list)}
            class_name_to_sequence_class_id = {class_name: class_id for class_id, class_name in class_id_to_class_name.items()}
            return class_id_to_class_name, class_name_to_sequence_class_id

        if str(self.class_txt_path) == ".":
            self.class_id_to_class_name, self.class_name_to_class_id = _scan_annotation_file()
            return
        if not self.class_txt_path.exists():
            self.class_id_to_class_name, self.class_name_to_class_id = _scan_annotation_file()
            return
        with open(self.class_txt_path) as f:
            lines = f.read().split('\n')
        # For MSCOCO, 1-origin
        self.class_id_to_class_name = {index+1: line.replace(' ', '-') for index, line in enumerate(lines) if line != ""}
        self.class_name_to_class_id = {class_name: class_id for class_id, class_name in self.class_id_to_class_name.items()}

    
    def _parse_annotation(self):
        self.logger.info("Parsing annotation file")
        annotation_path_list = sorted(self.src_path.glob("**/*txt"))
        annotation_id = 1
        for index, annotation_path in enumerate(annotation_path_list):
            image_extension = check_image_existence(annotation_path)
            if not image_extension:
                print(f"Image file corresponding to '{annotation_path}' not found. Ignored.")
                continue
            image_path = annotation_path.with_suffix(image_extension)
            image = cv2.imread(str(image_path))
            image_height, image_width = image.shape[:2]
            self.image_id_to_image_info[index] = {
                "file_name": image_path.name,
                "file_path": str(image_path.absolute()),
                "width": image_width,
                "height": image_height,
            }
            with open(annotation_path) as f:
                lines = f.read().split('\n')
            for line in lines:
                if line == "":
                    continue
                split_line = line.split(" ")
                score = None
                # Space in class name is not allowed
                if len(split_line) == 17:
                    score = float(split_line[-1])
                    split_line = split_line[:-1]
                class_name = split_line[0]
                class_id = self.class_name_to_class_id[class_name]
                bbox = [float(b) for b in split_line[4:8]]
                bbox = topleftbottomright2topleftwh(bbox)
                self.image_id_to_annotation_list[index].append({
                    "annotation_id": annotation_id,
                    "class_id": class_id,
                    "bbox": bbox,
                    "score": score,
                })
                annotation_id += 1
            

    def convert(self, dst_format):
        self.mscoco_data.convert(dst_format)

    def validation_check(self):
        if not self.src_path.exists():
            self.logger.critical(f"Annotation directory '{self.src_path}' not found")
            super()._finalize()
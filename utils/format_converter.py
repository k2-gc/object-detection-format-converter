from utils.kitti import KITTIDataset
from utils.mscoco import MSCOCODataset 
from utils.pascalvoc import PascalVOCDataset
from utils.yolo import YoloDataset

class ObjDetFormatConverter():
    """Converter class from 'dst_format' to 'src_format'

    Args:
        src_format (str): Input dataset format. e.g. 'yolo'
        dst_format (str): Output dataset format. e.g. 'coco'
        src_path (str): Input dataset path
        dst_path (str): Output dataset path
        class_txt_path (str): Class list file txt (optional)
                              See 'base.py' as well.
    """
    def __init__(self, src_format: str, dst_format: str, src_path: str, dst_path: str, class_txt_path: str = "") -> None:
        self.src_format = src_format
        self.dst_format = dst_format
        self.src_path = src_path
        self.dst_path = dst_path
        self.class_txt_path = class_txt_path
        self.src_dataset_class = self.create_src_dataset_class()
    
    def create_src_dataset_class(self):
        if self.src_format == "coco":
            return MSCOCODataset(self.dst_path, self.class_txt_path, self.src_path)
        elif self.src_format == "yolo":
            return YoloDataset(self.dst_path, self.class_txt_path, self.src_path)
        elif self.src_format == "kitti":
            return KITTIDataset(self.dst_path, self.class_txt_path, self.src_path)
        elif self.src_format == "pascalvoc":
            return PascalVOCDataset(self.dst_path, self.class_txt_path, self.src_path)
        
    def run_convert(self):
        self.src_dataset_class.convert(self.dst_format)
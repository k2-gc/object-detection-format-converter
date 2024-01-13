from collections import defaultdict
import logging
from pathlib import Path

class BaseDataFormat:
    """Data format super class

    Args:
        dst_path (str): Converted dataset output path
        class_txt_path (str): Class list text path
                              The file contains all class names in each line
            Example:
                ```txt
                person
                bicycle
                car
                motorcycle
                airplane
                ```
        src_path (str): Input dataset path to be converted
    """
    def __init__(self, dst_path, class_txt_path, src_path) -> None:
        self.src_path = Path(src_path)
        self.dst_path = Path(dst_path)
        self.class_txt_path = Path(class_txt_path)
        self.image_id_to_image_info = dict()
        self.image_id_to_annotation_list = defaultdict(list)
        self.class_id_to_class_name = dict()
        self.class_name_to_class_id = dict()
        self.logger = logging.getLogger("logger")
        self.validation_check()
        
    def _parse_annotation(self):
        pass
    
    def _parse_class_list(self):
        pass

    def convert(self):
        pass

    def validation_check(self):
        pass

    def _finalize(self):
        self.logger.info("Program stopped")
        exit()
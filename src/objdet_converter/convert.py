import logging

from .utils.utils import check_format_validation
from .utils.format_converter import ObjDetFormatConverter


def convert_format(src_format, dst_format, src_path, dst_path, class_txt_path=""):
    logger = logging.getLogger("logger")
    if not logger.hasHandlers():
        st_handler = logging.StreamHandler()
        format = "[%(levelname)s] %(message)s"
        st_handler.setFormatter(logging.Formatter(format))
        logger.setLevel(logging.INFO)
        logger.addHandler(st_handler)

    if src_format == dst_format:
        logger.error("Input format and Output format are same")
        return False
    if not check_format_validation(src_format):
        return False
    if not check_format_validation(dst_format):
        return False
    obj_det_format_converter = ObjDetFormatConverter(
        src_format,
        dst_format,
        src_path,
        dst_path,
        class_txt_path,
    )
    obj_det_format_converter.run_convert()
    logger.info("Converting completed")


from .utils import check_format_validation
from .format_converter import ObjDetFormatConverter


def convert_format(src_format, dst_format, src_path, dst_path, class_txt_path=""):
    if src_format == dst_format:
        print("Input format and Output format are same")
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


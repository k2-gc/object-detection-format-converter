import logging
from typing import Union

from pathlib import Path

supported_data_format_list = [
    "coco",
    "yolo",
    "pascalvoc",
    "kitti",
]

supported_ext_list = [
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
    ".tif",
]


def check_format_validation(format: str) -> bool:
    """Check whether specified format is supported or not

    Args:
        format (str): Dataset format name
    
    Returns:
        bool: Dataset format is supported = True, else = False
    """
    logger = logging.getLogger("logger")
    if not format in supported_data_format_list:
        logger.error(f"Format '{format}' not Supported")
        logger.error(f"Supported data format: [{', '.join(supported_data_format_list)}]")
        return False
    logger.info(f"Format '{format}' valid")
    return True

def check_image_existence(file_path: Path) -> Union[None, str]:
    """Check whether image exists or not.
       Get annotation file path, add supported image extension to the path and check existence

    Args:
        file_path (pathlib.Path): Annotation file path

    Returns:
        None | str: If image exists, return its extension, else None
    """
    for ext in supported_ext_list:
        if file_path.with_suffix(ext).exists():
            return ext
    return None

def topleftwh2centerwh(bbox: list) -> list:
    """Convert bbox coordinates
        [left, top, width, height] -> [center_x, center_y, width, height]
    
    Args:
        bbox (list): Bbox points [left, top, width, height]
    
    Returns:
        list: [center_x, center_y, width, height]
    """
    left = bbox[0]
    top = bbox[1]
    width = bbox[2]
    height = bbox[3]
    center_x = left + width / 2
    center_y = top + height / 2
    return [center_x, center_y, width, height]

def centerwh2topleftwh(bbox: list) -> list:
    """Convert bbox coordinates
        [center_x, center_y, width, height] -> [left, top, width, height]
    
    Args:
        bbox (list): Bbox points [center_x, center_y, width, height]

    Returns:
        list: [left, top, width, height]
    """
    center_x = bbox[0]
    center_y = bbox[1]
    width = bbox[2]
    height = bbox[3]
    left = center_x - width / 2
    top = center_y - height / 2
    return [left, top, width, height]

def topleftbottomright2topleftwh(bbox: list) -> list:
    """Convert bbox coordinates
        [left, top, right, bottom] -> [left, top, width, height]
    
    Args:
        bbox (list): Bbox points [left, top, right, bottom]

    Returns:
        list: [left, top, width, height]
    """
    left = bbox[0]
    top = bbox[1]
    right = bbox[2]
    bottom = bbox[3]
    width = right - left
    height = bottom - top
    return [left, top, width, height]

def topleftwh2topleftbottomright(bbox: list) -> list:
    """Convert bbox coordinates
        [left, top, width, height] -> [left, top, right, bottom]
    
    Args:
        bbox (list): Bbox points [left, top, width, height]

    Returns:
        list: [left, top, right, bottom]
    """
    left = bbox[0]
    top = bbox[1]
    width = bbox[2]
    height = bbox[3]
    right = left + width
    bottom = top + height
    return [left, top, right, bottom]

def absolute2relative(bbox: list, image_width: Union[int, float], image_height: Union[int, float]) -> list:
    """Convert bbox coordinates from absolute to relative
    
    Args:
        bbox (list): Absolute bbox points [x1, y1, x2, y2]
        image_width (int | float): Image width
        image_height (int | float): Image height
    
    Returns:
        list: Relative bbox points [x1, y1, x2, y2]. Range between [0, 1]
    """
    relative_x1 = bbox[0] / image_width
    relative_y1 = bbox[1] / image_height
    relative_x2 = bbox[2] / image_width
    relative_y2 = bbox[3] / image_height
    return [relative_x1, relative_y1, relative_x2, relative_y2]

def relative2absolute(bbox: list, image_width: Union[int, float], image_height: Union[int, float]) -> list:
    """Convert bbox coordinates from relative to absolute
    
    Args:
        bbox (list): Relative bbox points [x1, y1, x2, y2]
        image_width (int | float): Image width
        image_height (int | float): Image height

    Returns:
        list: Absolute bbox pinrts [x1, y1, x2, y2]. Range between [0, image_height or image_width]
    """
    absolute_x1 = bbox[0] * image_width
    absolute_y1 = bbox[1] * image_height
    absolute_x2 = bbox[2] * image_width
    absolute_y2 = bbox[3] * image_height
    return [absolute_x1, absolute_y1, absolute_x2, absolute_y2]

def calculate_area(bbox) -> float:
    """Calculate bbox area

    Args:
        bbox (list): Bbox points. Expected topleft-wh
    
    Returns:
        float: Bbox area. Image width * Image height
    """
    return bbox[2] * bbox[3]

def get_rectangle_all_points(bbox):
    """Get 4 coordinates of provided bbox rectangle

    Args:
        bbox (list): Bbox points. Expected topleft-bottomright
    
    Returns:
        list: 4 coordinates that composes bbox rectangle
    """
    return [
        bbox[0], bbox[1],
        bbox[2], bbox[1],
        bbox[2], bbox[3],
        bbox[0], bbox[3],
    ]
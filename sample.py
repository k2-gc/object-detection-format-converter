import argparse

from objdet_converter.utils.convert import convert_format


def convert_dataset(args):
    """Sample program to show usage
    """
    convert_format(
        src_format=args.src_format,
        dst_format=args.dst_format,
        src_path=args.src_path,
        dst_path=args.dst_path,
    )

def get_parser():
    parser = argparse.ArgumentParser(
        prog="Object Detection Dataset format converter sample program\n",
        description="Show how to use dataset format convert",
    )
    parser.add_argument("--src-format", type=str, required=True, help="Source dataset format. \
                        ['coco', 'yolo', 'pascalvoc', 'kitti']")
    parser.add_argument("--dst-format", type=str, required=True, help="Converted dataset format. \
                        ['coco', 'yolo', 'pascalvoc', 'kitti']")
    parser.add_argument("--src-path", type=str, required=True, help="Path to source dir/file")
    parser.add_argument("--dst-path", type=str, required=True, help="Path to output dir/file")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = get_parser()
    convert_dataset(args)
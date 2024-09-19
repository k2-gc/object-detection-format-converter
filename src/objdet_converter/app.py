import fire

from .convert import convert_format
from .utils.utils import supported_data_format_list

def help():
    print("Usage:")
    print("objdet-conv convert --src-format 'SRC_FORMAT' --dst-format 'DST_FORMAT' --src-path 'PATH_TO_SRC' --dst-path 'PAST_TO_OUTPUT' --class-txt-path 'IF NEEDED'")
    print(f"Supported format: {', '.join(supported_data_format_list)}")

convert_app = {
    "help": help,
    "convert": convert_format,
}

def app() -> None:
    """Cli app."""
    fire.Fire(convert_app)


if __name__ == "__main__":
    app()
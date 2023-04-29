import logging
from contextlib import contextmanager

logging.basicConfig(
    # format="[%(levelname)s:%(name)s] %(asctime)s: %(message)s",
    format="%(message)s",
    datefmt="%m/%d/%Y_%I:%M:%S_%p",
    level=logging.INFO,
)

log = logging.getLogger(__name__)


class TermColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[34m"
    OKYELLOW = "\033[33m"
    OKWHITE = "\033[37m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[32m"
    WARNING = "\033[93m"
    FAIL = "\033[31m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @classmethod
    def df_header(cls, header_text: str) -> str:
        return f"\n{cls.OKGREEN}{cls.BOLD}{header_text}{cls.ENDC}\n"

    @classmethod
    def _log_failure(cls, e: Exception) -> None:
        print(f"{cls.FAIL}{cls.BOLD}{e}{cls.ENDC}")

    @classmethod
    @contextmanager
    def with_failures(cls):
        try:
            yield
        except Exception as e:
            cls._log_failure(e)


class TermLogger:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        self._name = name

    @staticmethod
    def create_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    def infoc(self, msg: str, color: str = "", color_all: bool = False):
        if color == "":
            return self.info(msg, bold=True, color_value=True, color_all=color_all)
        self.info(msg, bold=True, color=color, color_value=True, color_all=color_all)

    def info(self, msg: str, *args, **kwargs):
        # We look for the `:` to only color after it
        color_all = kwargs.get("color_all", False)
        del kwargs["color_all"]
        if color_all:
            del kwargs["color_value"]

        color_value = False
        if kwargs.get("color_value", None) and not color_all:
            del kwargs["color_value"]
            color_value = True

            # TODO: Handle unicode chars and length etc.
            # Get the index and the parts of the message
            # value_idx = msg.index(":") + 1
            # print(len(msg.encode("utf-8")))
            # print(len(msg))
            # print(len("🛠️".encode("utf-8")))

            value_idx = msg.index(":") + 2

            msg_before = msg[:value_idx]
            msg = msg[value_idx:]

        if kwargs.get("bold", None):
            del kwargs["bold"]
            msg = f"{TermColors.BOLD}{msg}{TermColors.ENDC}"

        if color := kwargs.get("color", None):
            del kwargs["color"]
            match color:
                case "yellow":
                    msg = f"{TermColors.OKYELLOW}{msg}{TermColors.ENDC}"
                case "blue":
                    msg = f"{TermColors.OKBLUE}{msg}{TermColors.ENDC}"
                case "green":
                    msg = f"{TermColors.OKGREEN}{msg}{TermColors.ENDC}"
                case _:
                    raise ValueError(f"Unknown color [{color}]")

        if color_value:
            msg = msg_before + msg

        self._logger.info(msg, *args, *kwargs)

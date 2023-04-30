import functools
import os
import subprocess
import sys
import tarfile
from enum import Enum, auto
from pathlib import Path
from typing import Dict

import requests

FILE_LOCATION = os.path.dirname(__file__)
RUN = functools.partial(subprocess.run, capture_output=True, shell=True)


class BenchmarkTools:
    class SupportedTool(Enum):
        Vegeta = auto()
        Unknown = auto()

        @classmethod
        def tools(cls) -> Dict[str, "BenchmarkTools.SupportedTool"]:
            return {
                cls.Vegeta.name.lower(): cls.Vegeta,
            }

        @classmethod
        def from_value(cls, value: str) -> "BenchmarkTools.SupportedTool":
            return cls.tools().get(value, cls.Unknown.name.lower())

    def __init__(self, benchmark_tool: str):
        self._benchmark_tool = benchmark_tool

    @property
    def benchmark_tool(self) -> str:
        return self._benchmark_tool

    def is_found_locally(self) -> bool:
        local_path = Path(f"{FILE_LOCATION}/{self.benchmark_tool}")
        if local_path.exists():
            os.environ["PATH"] += os.pathsep + os.pathsep.join([str(local_path)])
            result = RUN(f"which {self.benchmark_tool}")
            if result.returncode == 0:
                return True
        return False

    def is_found_or_download(self) -> bool:
        # Check if it is installed globally
        result = RUN(f"which {self.benchmark_tool}")
        if result.returncode == 0:
            return True

        # Make sure the tool is not included locally
        if self.is_found_locally():
            return True

        # If tool is not found then attempt to download and install it
        self.download()

        # Now check to see if it is found again:
        if self.is_found_locally():
            return True

        return False

    def download(self) -> None:
        match self.__class__.SupportedTool.from_value(self.benchmark_tool):
            case self.__class__.SupportedTool.Vegeta:
                version = "12.8.4"
                download_path = (
                    f"https://github.com/tsenart/{self.benchmark_tool}/releases/download/"
                    + f"v{version}/{self.benchmark_tool}_{version}_linux_386.tar.gz"
                )
                vegeta_tar_gz = Path(
                    f"{FILE_LOCATION}/{self.benchmark_tool}_v{version}.tar.gz"
                )
                print(
                    f"Benchmark tool [{self.benchmark_tool}] not found on path. "
                    + f"Attempting to download version: v{version}"
                )

                # If path does not exist then download
                if not vegeta_tar_gz.exists():
                    resp = requests.get(
                        download_path, allow_redirects=True, stream=True
                    )
                    if resp.status_code == 200:
                        vegeta_tar_gz.write_bytes(resp.content)
                    else:
                        print(
                            f"Unable to download benchmark tool [{self.benchmark_tool}] from url: {download_path}"
                        )
                        sys.exit(1)

                # Make the directory to tar into
                vegeta_dir = Path(f"{FILE_LOCATION}/{self.benchmark_tool}")
                vegeta_dir.mkdir(exist_ok=True)

                # Now untar / unzip the downloaded tool
                with tarfile.open(vegeta_tar_gz) as tar_tool:
                    print(tar_tool.getnames())
                    tar_tool.extractall(vegeta_dir)
            case _:
                print(f"Unable to get benchmark tool: {self.benchmark_tool}")
                sys.exit(1)

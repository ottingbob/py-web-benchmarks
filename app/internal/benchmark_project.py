import functools
import os
import subprocess
import sys
from pathlib import Path, PurePath
from typing import List

BASE_DIR_LOCATION = Path(os.path.dirname(__file__)).parent.parent
RUN = functools.partial(subprocess.run, capture_output=True, shell=True)


class Project:
    def __init__(self, project_directory: str):
        self._project_directory = project_directory
        # Verify project on entry
        self.verify_project()

    def __str__(self):
        return self._project_directory

    @property
    def project_directory(self) -> str:
        return self._project_directory

    @property
    def docker_image(self) -> str:
        return f"pywebbench/{self._project_directory}:0.1"

    @staticmethod
    def get_projects() -> List[str]:
        # TODO: Fix `bjoern-hug-3.7`
        exclude = [".git", "__pycache__", ".ruff_cache", "bjoern-hug-3.7"]
        projects = []
        for path, dirs, files in os.walk(BASE_DIR_LOCATION, topdown=True):
            # This is described in: `help(os.walk)`
            # dirs[:] = value modifies dirs in-place. It changes the contents of the list dirs without changing the container
            dirs[:] = [d for d in dirs if d not in exclude]

            # Check for an `app/main.py` directory / file in project
            # Check for a dockerfile in project
            main_path = Path(path + "/app/main.py")
            if "app" in dirs and "Dockerfile" in files and main_path.exists():
                path = PurePath(path)
                projects.append(path.name)
        return projects

    def verify_project(self):
        # Make sure that the directory exists
        project_directory_path = Path(f"{BASE_DIR_LOCATION}/{self.project_directory}")
        if not project_directory_path.exists() or not project_directory_path.is_dir():
            print(
                f"Project directory: [{project_directory_path}] needs to exist and be a directory."
            )
            sys.exit(1)

        # Make sure the docker file exists
        project_dockerfile_path = Path(
            f"{BASE_DIR_LOCATION}/{self.project_directory}/Dockerfile"
        )
        if not project_directory_path.exists() or not project_directory_path.is_dir():
            print(f"Did not find Dockerfile at: [{project_dockerfile_path}]")
            sys.exit(1)

    def docker_build(self) -> str:
        result = RUN(
            f"docker build -q -f {self.project_directory}/Dockerfile"
            + f' -t "{self.docker_image}" {self.project_directory}'
        )
        if result.returncode != 0:
            print(
                f"Failed to build [{self.docker_image}]: {str(result.stderr.decode())}"
            )
            sys.exit(1)
        return result.stdout.decode().replace("\n", "")

    def docker_run(self) -> str:
        result = RUN(f'docker run -d -p 7331:7331 "{self.docker_image}"')
        if result.returncode != 0:
            print(f"Failed to run [{self.docker_image}]: {str(result.stderr.decode())}")
            sys.exit(1)
        return result.stdout.decode()[:13]

    # Should probably hold the container id internally...
    def docker_stop(self, container_id: str) -> str:
        result = RUN(f'docker stop "{container_id}"')
        if result.returncode != 0:
            print(f"Failed to stop [{container_id}]: {str(result.stderr.decode())}")
            sys.exit(1)

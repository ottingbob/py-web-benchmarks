import functools
import os
import subprocess
import sys
from pathlib import Path, PurePath
from typing import List

from app.internal.benchmark_tools import BenchmarkTools
from app.internal.markdown_generation import Markdown
from app.internal.term_colors import TermLogger

BASE_DIR_LOCATION = Path(os.path.dirname(__file__)).parent.parent
FILE_LOCATION = BASE_DIR_LOCATION
RUN = functools.partial(subprocess.run, capture_output=True, shell=True)
log = TermLogger(__name__)


def get_projects() -> List[str]:
    # TODO: Fix `bjoern-hug-3.7`
    exclude = [".git", "__pycache__", ".ruff_cache", "bjoern-hug-3.7"]
    projects = []
    for path, dirs, files in os.walk(FILE_LOCATION, topdown=True):
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


def verify_project(project_directory: str):
    # Make sure that the directory exists
    project_directory_path = Path(f"{FILE_LOCATION}/{project_directory}")
    if not project_directory_path.exists() or not project_directory_path.is_dir():
        print(
            f"Project directory: [{project_directory_path}] needs to exist and be a directory."
        )
        sys.exit(1)

    # Make sure the docker file exists
    project_dockerfile_path = Path(f"{FILE_LOCATION}/{project_directory}/Dockerfile")
    if not project_directory_path.exists() or not project_directory_path.is_dir():
        print(f"Did not find Dockerfile at: [{project_dockerfile_path}]")
        sys.exit(1)


def run_project_benchmark(project_directory: str):
    # Verify the project first
    verify_project(project_directory)

    # Build the docker image
    docker_image = f"pywebbench/{project_directory}:0.1"
    log.infoc(f"🛠️ Building docker image: {docker_image}", "blue")
    result = RUN(
        f'docker build -q -f {project_directory}/Dockerfile -t "{docker_image}" {project_directory}'
    )
    if result.returncode != 0:
        print(f"Failed to build [{docker_image}]: {str(result.stderr.decode())}")
        sys.exit(1)
    success = result.stdout.decode().replace("\n", "")
    log.infoc(f"✅ Build success with hash: {success}", "yellow")

    # Run the docker image
    log.infoc(
        f"🚀 Running docker image in background for benchmark: {docker_image}", "blue"
    )
    result = RUN(f'docker run -d -p 7331:7331 "{docker_image}"')
    if result.returncode != 0:
        print(f"Failed to run [{docker_image}]: {str(result.stderr.decode())}")
        sys.exit(1)
    container_id = result.stdout.decode()[:13]

    log.infoc(f"🇬🇴 Creating benchmark report for project: {project_directory}", "green")

    # TODO: Make sure docker container is ready to receive requests
    import time

    time.sleep(2)

    # Get benchmark arguments
    # TODO: Benchmark construction should go into a different file
    # TODO: Depending the the benchmark tool this should be loaded from a default config
    benchmark_args = {
        "duration": "20s",
        # "workers": "100",
        "workers": "10",
        # "rate": "10000/s",
        # "rate": "1000/s",
        "rate": "5000/s",
    }
    benchmark_args_print = ", ".join(f"{k}: {v}" for k, v in benchmark_args.items())
    benchmark_args_cmd = " ".join(f"-{k}={v}" for k, v in benchmark_args.items())
    log.infoc(
        f"📝 Running benchmark with args: [{benchmark_args_print}]\n", color="yellow"
    )

    # Construct benchmark command
    benchmark_base = f"echo 'GET http://localhost:7331/' | vegeta attack {benchmark_args_cmd} | tee results.bin | vegeta report"
    benchmark_report_filters = " | grep -v 'read: connection reset by peer' | uniq"
    benchmark_command = benchmark_base + benchmark_report_filters
    result = RUN(benchmark_command)
    if result.returncode == 0:
        benchmark_output = result.stdout.decode()
        log.infoc(benchmark_output, color_all=True)
        log.infoc("🏁 Benchmark completed 🏁", color="green", color_all=True)
    else:
        print(
            f"Failed to execute benchmark command [{benchmark_command}]: {result.stderr.decode()}"
        )

    # Stop the container
    log.infoc(f"⏹️  Stopping docker container: [{container_id}]", "yellow")
    result = RUN(f'docker stop "{container_id}"')
    if result.returncode != 0:
        print(f"Failed to stop [{container_id}]: {str(result.stderr.decode())}")
        sys.exit(1)

    log.infoc(
        f"📸 Capturing benchmark report in markdown: [benchmark-reports/{project_directory}.md]",
        "header",
    )
    # Generate the report markdown
    Markdown.capture_project_benchmark_markdown(
        project_directory, benchmark_base, benchmark_output
    )


def report():
    # Double check to make sure benchmarking tool is installed
    print(FILE_LOCATION)
    benchmark_tool = "vegeta"
    if not BenchmarkTools(benchmark_tool).is_found_or_download():
        print(f"Unable to find or get/download: {benchmark_tool}")
        sys.exit(1)

    # TODO: Get better CLI validation
    if len(sys.argv) == 3:
        arg_2 = sys.argv[2]
        if arg_2 == "generate":
            Markdown(get_projects()).generate_readme()
            sys.exit(0)
        print(f"Unable to run command with arg: {arg_2}")
        sys.exit(1)
        ##### results from bjoern-3.7 benchmark

    # Ensure that we have a project passed in
    if len(sys.argv) < 2:
        print("Need to provide a [project directory] as arguments.")
        sys.exit(1)
    project_directory = sys.argv[1]

    # Check if project directory is `all` to run all projects
    if project_directory == "all":
        # Get the projects and run each benchmark
        for project in get_projects():
            run_project_benchmark(project)
            print()
    else:
        # Run the project benchmark
        run_project_benchmark(project_directory)


if __name__ == "__main__":
    report()

import functools
import os
import subprocess
import sys
from pathlib import Path

from app.internal.benchmark_project import Project
from app.internal.benchmark_tools import BenchmarkTools
from app.internal.markdown_generation import Markdown
from app.internal.term_colors import TermLogger

BASE_DIR_LOCATION = Path(os.path.dirname(__file__)).parent.parent
FILE_LOCATION = BASE_DIR_LOCATION
RUN = functools.partial(subprocess.run, capture_output=True, shell=True)
log = TermLogger(__name__)


def run_project_benchmark(project_directory: str):
    # Verify the project first
    project = Project(project_directory)

    # Build the docker image
    log.infoc(f"🛠️ Building docker image: {project.docker_image}", "blue")
    build_success_hash = project.docker_build()
    log.infoc(f"✅ Build success with hash: {build_success_hash}", "yellow")

    # Run the docker image
    log.infoc(
        f"🚀 Running docker image in background for benchmark: {project.docker_image}",
        "blue",
    )
    container_id = project.docker_run()

    log.infoc(f"🇬🇴 Creating benchmark report for project: {project}", "green")

    # TODO: Make sure docker container is ready to receive requests
    import time

    time.sleep(2)

    # Get benchmark arguments
    # TODO: Benchmark construction should go into a different file
    # TODO: Depending the the benchmark tool this should be loaded from a default config
    benchmark_args = {
        "duration": "5s",
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
    project.docker_stop(container_id)

    log.infoc(
        f"📸 Capturing benchmark report in markdown: [benchmark-reports/{project}.md]",
        "header",
    )
    # Generate the report markdown
    Markdown.capture_project_benchmark_markdown(
        project_directory, benchmark_base, benchmark_output
    )


def report():
    # Double check to make sure benchmarking tool is installed
    benchmark_tool = "vegeta"
    if not BenchmarkTools(benchmark_tool).is_found_or_download():
        print(f"Unable to find or get/download: {benchmark_tool}")
        sys.exit(1)

    # TODO: Get better CLI validation
    if len(sys.argv) == 3:
        arg_2 = sys.argv[2]
        if arg_2 == "generate":
            Markdown(Project.get_projects()).generate_readme()
            sys.exit(0)
        print(f"Unable to run command with arg: {arg_2}")
        sys.exit(1)

    # Ensure that we have a project passed in
    if len(sys.argv) < 2:
        print("Need to provide a [project directory] as arguments.")
        sys.exit(1)
    project_directory = sys.argv[1]

    # Check if project directory is `all` to run all projects
    if project_directory == "all":
        # Get the projects and run each benchmark
        for project in Project.get_projects():
            run_project_benchmark(project)
            print()
    else:
        # Run the project benchmark
        run_project_benchmark(project_directory)


if __name__ == "__main__":
    report()

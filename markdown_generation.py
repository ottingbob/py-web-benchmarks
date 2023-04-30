import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

FILE_LOCATION = os.path.dirname(__file__)


class Markdown:
    def __init__(self, projects: List[str]):
        self._projects = projects

    @property
    def projects(self) -> List[str]:
        return self._projects

    def _get_project_stubs_from_readme(
        self,
        readme_text: str
        # FIXME: Learn how to clean up this type...
    ) -> Tuple[List[Dict[str, Any]], int, int]:
        # TODO: Clean up the output so there are only benchmark stubs
        stubs = []
        for idx, line in enumerate(readme_text):
            if re.findall("^#### Raw Project Benchmark Results", line):
                start_idx = idx
                continue
            if re.findall("^### Resources", line):
                end_idx = idx
                continue
            for project in self.projects:
                if matches := re.findall(f"^#####.*{project} benchmark", line):
                    if len(matches) > 1:
                        raise RuntimeError(
                            "Should not find more than 1 benchmark stub on a given line in [README.md]: ",
                            idx,
                            matches,
                        )
                    stubs.append({project: {"stub": matches[0], "line": idx}})
        return (stubs, start_idx, end_idx)

    def _clear_project_stubs_from_readme(
        self, matches: List[Dict[str, Any]], readme_text: List[str], end_idx: int
    ) -> str:
        # TODO: Why is the data structure above so complicated to try and get the line idx...
        readme_full = "\n".join(readme_text)
        for previous, current in zip(matches, matches[1:]):
            previous_line = [mv.get("line", 0) for mv in previous]
            current_line = [mv.get("line", 0) for mv in current]

            project_benchmark_md = readme_text[previous_line[0] : current_line[0]]
            project_benchmark_stub = [
                mv.get("stub", "##### unknown benchmark") for mv in previous
            ][0]

            readme_full = readme_full.replace(
                "\n".join(project_benchmark_md), project_benchmark_stub
            )
            final_project_idx = current_line[0]
            final_project_stub = [
                mv.get("stub", "##### unknown benchmark") for mv in current
            ][0]

        # Replace final range
        readme_full = readme_full.replace(
            "\n".join(readme_text[final_project_idx:end_idx]),
            # We add an extra newline before the resources section
            final_project_stub + "\n",
        )
        return readme_full

    def clear_benchmark_results(self):
        # Read in the readme text into an array by each line
        readme_md = Path(f"{FILE_LOCATION}/README.md")
        readme_text = readme_md.read_text().split("\n")

        # Get the project stub objects (line & stub header) and the range from where
        # the benchmark results start (start_idx) and the references section begins (end_idx)
        stubs, start_idx, end_idx = self._get_project_stubs_from_readme(readme_text)

        # Get the matches for the previous benchmark output and replace them with just
        # the stubs
        matches = [project.values() for project in stubs if any(project.values())]
        readme_benchmark_stubs = self._clear_project_stubs_from_readme(
            matches, readme_text, end_idx
        )
        readme_md.write_text(readme_benchmark_stubs)

    def generate_readme(self):
        # Start by clearing the previous benchmark results
        self.clear_benchmark_results()

        # Now update the readme with results from the `benchmark-reports/` directory

        # Read in the readme text into an array by each line
        readme_md = Path(f"{FILE_LOCATION}/README.md")
        readme_text = readme_md.read_text().split("\n")

        for idx, line in enumerate(readme_text):
            # Oof this is not good
            for project in self.projects:
                if re.findall(f"^#####.*{project} benchmark", line):
                    # Get related project markdown
                    benchmark_md_path = Path(
                        f"{FILE_LOCATION}/benchmark-reports/{project}.md"
                    )
                    project_bench_md = benchmark_md_path.read_text()
                    readme_text[idx] = project_bench_md

        readme_md.write_text("\n".join(readme_text))

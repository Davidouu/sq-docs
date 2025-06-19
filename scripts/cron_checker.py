from pathlib import Path
from check_commits import CheckCommits

runner = CheckCommits(
    repo_root=Path(__file__).resolve().parent,
    output_root=Path("./"),
)
runner.run()

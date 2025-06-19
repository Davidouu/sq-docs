from pathlib import Path
from check_commits import CheckCommits

if __name__ == "__main__":
    # ► racine = dossier parent de "scripts"
    repo_root = Path(__file__).resolve().parent.parent

    checker = CheckCommits(
        repo_root=repo_root,
        output_root=repo_root,
    )
    checker.run()
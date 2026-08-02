import os
import subprocess

from github import Github
from invoke import Context, task

from .data import migrate
from .utils import info


def latest_master_sha():
    """
    Get latest commit SHA from origin/master.
    """
    result = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/master"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.split()[0]


def github_repo():
    """
    Get owner/repo from git origin.
    """
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    # supports:
    # git@github.com:owner/repo.git
    # https://github.com/owner/repo.git
    remote = remote.removesuffix(".git")

    if remote.startswith("git@github.com:"):
        remote = remote.removeprefix("git@github.com:")
    elif remote.startswith("https://github.com/"):
        remote = remote.removeprefix("https://github.com/")
    else:
        raise RuntimeError(f"Unsupported GitHub remote: {remote}")

    return remote.split("/", 1)


def github_actions_status(owner: str, repo: str, sha: str):
    """
    Check GitHub Actions status for a commit.
    """
    token = os.environ.get("GITHUB_TOKEN")
    github = Github(token) if token else Github()
    repository = github.get_repo(f"{owner}/{repo}")
    checks = repository.get_commit(sha).get_check_runs()

    if checks.totalCount == 0:
        return "missing"

    for check in checks:
        if check.status != "completed":
            return "pending"

        if check.conclusion != "success":
            return check.conclusion

    return "success"


@task(aliases=["u"])
def update(c: Context):
    """
    Update LibrePlate dependencies, source code, and database state.
    """
    info("Checking latest master build")

    sha = latest_master_sha()

    owner, repo = github_repo()

    status = github_actions_status(owner, repo, sha)

    if status != "success":
        info(
            f"Latest master commit {sha[:7]} "
            f"is not verified ({status}), skipping update"
        )
        return

    info(f"Latest master commit {sha[:7]} passed CI")

    info("Updating LibrePlate")

    c.run("git pull origin master")
    c.run("uv sync")
    migrate(c)

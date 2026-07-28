import re
from pathlib import Path

from invoke import Context, task
from utils import BASE_DIR, print_success

TASK_PATTERN = re.compile(r"^\s{2}(?P<name>[a-zA-Z_][\w.-]*)\s{2,}")

MANUAL_HEADER = """
<!-- AUTOMATICALLY GENERATED FILE, CHECK INVOKE HOW TO UPDATE. -->

# Invoke tasks documentation

To use invoke you will have to create a virtual environment first, and use its
python shell. I recommand install uv and run:
```
cd backend && uv sync
source ./venv/bin/activate
cd ../
```

To run a task you can run:
```
invoke <task> <flags>
```

To learn more about that invoke task you can run:

```
invoke --help <task>
```

If you are new to invoke you can also run:

```
invoke -help
```

"""


@task(aliases=["geninv"])
def generate_invoke_manual(c: Context, check: bool = False) -> None:
    """
    Generate a Markdown manual of all Invoke tasks.

    Args:
        check: Only check whether the generated manual differs from the existing file.
    """

    output = Path(BASE_DIR / "INVOKE_MANUAL.md")
    result = c.run("invoke --list", hide=True)
    tasks = []

    for line in result.stdout.splitlines():
        match = TASK_PATTERN.match(line)
        if match:
            tasks.append(match.group("name"))

    markdown = [MANUAL_HEADER]

    for name in tasks:
        help_text = c.run(
            f"invoke --help {name}",
            hide=True,
            warn=True,
        ).stdout

        markdown.extend(
            [
                f"\n## `{name}`\n",
                "```text\n",
                help_text,
                "```\n",
            ]
        )

    generated = "\n".join(markdown)

    if check:
        if not output.exists():
            c.fail(f"`{output}` does not exist. Manual needs to be generated.")

        existing = output.read_text(encoding="utf-8")

        if existing != generated:
            c.fail(f"`{output}` is out of date. Run `invoke generate-invoke-manual`.")

        print_success("Invoke manual is up to date.")
        return

    output.write_text(generated, encoding="utf-8")

    print_success(f"Generated `{output}`")

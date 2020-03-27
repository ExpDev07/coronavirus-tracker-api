"""
tasks.py
--------
Project invoke tasks

Available commands
  invoke --list
  invoke fmt
  invoke sort
"""
import invoke

TARGETS_DESCRIPTION = "Paths/directories to format. [default: . ]"


@invoke.task(help={"targets": TARGETS_DESCRIPTION})
def sort(ctx, targets="."):
    """Sort module imports."""
    print("sorting imports ...")
    args = ["isort", "-rc", "--atomic", targets]
    ctx.run(" ".join(args))


@invoke.task(pre=[sort], help={"targets": TARGETS_DESCRIPTION})
def fmt(ctx, targets="."):
    """Format python source code & sort imports."""
    print("formatting ...")
    args = ["black", targets]
    ctx.run(" ".join(args))

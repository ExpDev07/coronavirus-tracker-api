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

@invoke.task
def check(ctx, fmt=False, sort=False):
    """Check code format and import order."""
    if not any([fmt, sort]):
        fmt = True
        sort = True

    fmt_args = ["black", "--check", "--diff", "."]
    sort_args = ["isort", "-rc", "--check", "--diff", "."]
    cmd_args = []

    if fmt:
        cmd_args.extend(fmt_args)
    if sort:
        if cmd_args:
            cmd_args.append("&")
        cmd_args.extend(sort_args)
    ctx.run(" ".join(cmd_args))

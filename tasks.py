"""
tasks.py
--------
Project invoke tasks

Available commands
  invoke --list
  invoke fmt
  invoke sort
  invoke check
"""
import random

import invoke

TARGETS_DESCRIPTION = "Paths/directories to format. [default: . ]"


@invoke.task(help={"targets": TARGETS_DESCRIPTION})
def sort(ctx, targets="."):
    """Sort module imports."""
    print("sorting imports ...")
    args = ["isort", "--atomic", targets]
    ctx.run(" ".join(args))


@invoke.task(pre=[sort], help={"targets": TARGETS_DESCRIPTION})
def fmt(ctx, targets="."):
    """Format python source code & sort imports."""
    print("formatting ...")
    args = ["black", targets]
    ctx.run(" ".join(args))


@invoke.task
def check(ctx, fmt=False, sort=False, diff=False):  # pylint: disable=redefined-outer-name
    """Check code format and import order."""
    if not any([fmt, sort]):
        fmt = True
        sort = True

    fmt_args = ["black", "--check", "."]
    sort_args = ["isort", "--check", "."]

    if diff:
        fmt_args.append("--diff")
        sort_args.append("--diff")

    # FIXME: run each command and check return code
    cmd_args = []
    if fmt:
        cmd_args.extend(fmt_args)
    if sort:
        if cmd_args:
            cmd_args.append("&")
        cmd_args.extend(sort_args)
    ctx.run(" ".join(cmd_args))


@invoke.task
def lint(ctx):
    """Run linter."""
    ctx.run(" ".join(["pylint", "app"]))


@invoke.task
def test(ctx):
    """Run pytest tests."""
    ctx.run(" ".join(["pytest", "-v"]))


@invoke.task
def generate_reqs(ctx):
    """Generate requirements.txt"""
    reqs = [
        "pipenv lock -r > requirements.txt",
        "pipenv lock -r --dev > requirements-dev.txt",
    ]
    [ctx.run(req) for req in reqs]


@invoke.task
def docker(
    ctx,
    build=False,
    run=False,
    tag="covid-tracker-api:latest",
    name=f"covid-api-{random.randint(0,999)}",
):
    """Build and run docker container."""
    if not any([build, run]):
        raise invoke.Exit(message="Specify either --build or --run", code=1)
    if build:
        docker_cmds = ["build", "."]
    else:
        docker_cmds = ["run", "--publish", "80", "--name", name]
    ctx.run(" ".join(["docker", *docker_cmds, "-t", tag]))

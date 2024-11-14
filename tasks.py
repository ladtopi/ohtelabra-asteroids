from invoke import task


@task
def start(ctx):
    ctx.run("python src/main.py", pty=True)


@task
def test(ctx):
    ctx.run("pytest", pty=True)


@task(aliases=["cov"])
def coverage_report(ctx, no_open=False):
    ctx.run("coverage run")
    ctx.run("coverage html")
    if not no_open:
        print("Opening coverage report in browser")
        import os
        import webbrowser
        path = os.path.join(os.getcwd(), "htmlcov/index.html")
        webbrowser.open("file:///" + path, new=2)

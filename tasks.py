from invoke import task


@task
def build(c):
    """Build local Docker environment"""
    c.run("docker build . --tag photos:latest -f docker/Dockerfile")


@task
def web(c):
    """Run Django website for local development"""
    c.run("docker-compose -f docker/docker-compose.local.yml up web")


@task
def logs(c):
    c.run("docker-compose -f docker/docker-compose.local.yml logs --tail 100 -f worker", pty=True)


@task
def debug(c):
    """Run Django with debugging enabled"""
    c.run(
        "docker-compose -f docker/docker-compose.local.yml run --rm --service-ports web", pty=True
    )


@task
def bash(c):
    """Get a bash shell in the docker container"""
    compose_run(c, "bash", pty=True)


@task
def shell(c):
    """Get a Django shell_plus shell in the docker container"""
    compose_run(c, "./manage.py shell_plus", pty=True)


@task
def psql(c):
    """Get a Postgres shell in the docker container"""
    compose_run(c, "psql", pty=True)


def compose_run(c, cmd: str, **kwargs):
    c.run(f"docker-compose -f docker/docker-compose.local.yml run --rm web {cmd}", **kwargs)


import nox


REQUIRES = {
    "coverage": ["coverage>=5.0.0,<6.0.0"],
    "fmt": ["black>=19.10b0,<20.00"],
    "lint": ["flake8>=3.7.9,<4.0.0"],
}


def install(session, *names):
    for e in names:
        session.install(*REQUIRES[e])


@nox.session
def devel(session):
    session.install("-e", ".")
    install(session, "coverage", "fmt", "lint")


@nox.session(python=["3.6", "3.7"])
def test(session):
    session.install("-e", ".")
    session.run("python", "-m", "unittest", "discover", "tests")


@nox.session
def coverage(session):
    session.install("-e", ".")
    install(session, "coverage")
    session.run(
        "coverage",
        "run",
        "--source=hexastore",
        "-m",
        "unittest",
        "discover",
        "tests",
    )
    session.run("coverage", "report", "-m")


@nox.session
def fmt(session):
    install(session, "fmt")
    session.run("black", ".")


@nox.session
def lint(session):
    install(session, "fmt", "lint")
    session.run("black", ".")
    session.run("flake8")

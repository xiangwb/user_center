import click
from flask.cli import FlaskGroup

from user.app import create_app


def create_user(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_user)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new admin user
    """
    from user.models import User

    click.echo("create user")
    user = User(username="admin", email="admin@mail.com", password="admin", active=True).save()
    click.echo("created user admin: {id}".format(id=user.id))


if __name__ == "__main__":
    cli()

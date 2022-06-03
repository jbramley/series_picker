import random

import click

import fetchers
from book_series.models import BookStatus
from book_series.repository import AbstractBookSeriesRepository, get_repository
from fetchers import get_fetcher

pass_repository = click.make_pass_decorator(AbstractBookSeriesRepository)


@click.group()
@click.option("-d", "--datastore", default="json:series.json")
@click.pass_context
def cli(ctx, datastore: str):
    ctx.obj = get_repository(datastore)


@cli.command()
@click.option(
    "-s", "--source", type=click.Choice(fetchers.FETCHERS, case_sensitive=False)
)
@click.argument("path_or_url")
@pass_repository
def add(repository: AbstractBookSeriesRepository, source: str, path_or_url: str):
    fetcher = get_fetcher(source)
    series = fetcher(path_or_url)
    repository.add(series)


@cli.command("list")
@click.option("-i", "--idle", "only_idle", is_flag=True)
@click.option("--details", "show_details", is_flag=True)
@pass_repository
def list_series(
    repository: AbstractBookSeriesRepository, only_idle: bool, show_details: bool
):
    series = repository.get_all_idle() if only_idle else repository.get_all()
    if show_details:
        for s in series:
            print(f" * {s.title}")
            print("\n".join(f"   * {b.title} [{b.status}]" for b in s.books))
    else:
        print("\n".join(f" * {s.title}" for s in series))


@cli.command("next")
@pass_repository
def next_book(repository: AbstractBookSeriesRepository):
    idle_series = repository.get_all_idle()
    next_series = random.choice(list(idle_series))
    next_title = next(
        b.title for b in next_series.books if b.status == BookStatus.UNREAD
    )
    print(f"Try _{next_title}_ from the {next_series.title} series")


if __name__ == "__main__":
    cli()

import random
from typing import Tuple

import click
from rich.console import Console
from rich.markup import escape
from rich.prompt import Prompt

import fetchers
from book_series.models import BookSeries, BookStatus
from book_series.repository import AbstractBookSeriesRepository, get_repository
from cli_formatter import (
    detail_formatter,
    list_formatter,
    mk_kobo_direct_url,
    mk_kobo_search_url,
    mk_libby_book_search_url,
)
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
    series_list = list_formatter(series)
    if show_details:
        series_list = detail_formatter(series_list)

    print("\n".join(s[0] for s in series_list))


@cli.command("next")
@click.option("--link-text/--no-link-text", default=True)
@pass_repository
def next_book(repository: AbstractBookSeriesRepository, link_text: bool):
    console = Console()
    while True:
        next_series, next_title = _get_book_recommendation(repository)
        _print_book_recommendation(console, link_text, next_series, next_title)
        action = _get_recommendation_action(console)
        if action == "R":
            repository.update_book_status(next_series, next_title, BookStatus.READING)
            break
        if action == "O":
            repository.update_book_status(next_series, next_title, BookStatus.ON_HOLD)
            break
        if action == "N":
            continue
        if action == "Q":
            break


@cli.command("upgrade")
@pass_repository
def upgrade(repository: AbstractBookSeriesRepository):
    repository.upgrade()
    repository


def _get_book_recommendation(repository) -> Tuple[BookSeries, str]:
    idle_series = repository.get_all_idle()
    next_series = random.choice(list(idle_series))
    next_title = next(
        b.title for b in next_series.books if b.status == BookStatus.UNREAD
    )
    return next_series, next_title


def _get_recommendation_action(console):
    console.print("\nUpdate Status?")
    console.print("[R]eading")
    console.print("[O]n hold")
    console.print("[N]ew recommendation")
    console.print("[Q]uit")
    return Prompt.ask("Choice> ", choices=["R", "O", "N", "Q"])


def _print_book_recommendation(console, link_text, next_series, next_title):
    console.print(
        f"Try [bold italic]{escape(next_title)}[/bold italic] from the {next_series.title} series"
    )
    urls = {
        "Libby": mk_libby_book_search_url(next_title),
        "Kobo": mk_kobo_direct_url(next_title),
        "Kobo Search": mk_kobo_search_url(next_title),
    }
    console.print(
        escape("  ["),
        " | ".join(
            url_link(link_title, link_value, link_text)
            for link_title, link_value in urls.items()
        ),
        escape("]"),
    )


def url_link(title: str, url: str, as_link: bool) -> str:
    return url_link_text(title, url) if as_link else url_link_plain(title, url)


def url_link_text(title: str, url: str) -> str:
    return f"[link={escape(url)}]{escape(title)}[/link]"


def url_link_plain(title: str, url: str) -> str:
    return f"{escape(title)}: {escape(url)}\n "


if __name__ == "__main__":
    cli()

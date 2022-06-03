import click

import fetchers
from book_series.repository import AbstractBookSeriesRepository, get_repository
from fetchers import get_fetcher

# def main(data_file: str):
#     book_series_repository = JsonBookSeriesRepository(data_file)
#     print([s.title for s in book_series_repository.get_all()])
#     print([s.title for s in book_series_repository.get_all_idle()])
#
#     new_series = goodreads_fetcher("https://www.goodreads.com/series/56399-the-expanse")
#     print(new_series)
#     # book_series_repository.add(new_series)
#     print([s.title for s in book_series_repository.get_all()])

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


if __name__ == "__main__":
    cli()

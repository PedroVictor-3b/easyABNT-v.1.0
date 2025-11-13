from enum import Enum
from datetime import date

import aiohttp

from .schemas import JournalArticle


class CrossrefTypes(Enum):
    journal_article = "journal-article"


class CrossrefService:
    class Exceptions:
        class CrossrefException(Exception):
            pass

    @classmethod
    def _format_journal_article(cls, data: dict):
        data = data.get("message")  # type: ignore

        # get author names
        authors = data.get("author")
        main_author = ""
        other_authors = []
        for author in authors:  # type: ignore
            author_name = f'{author.get("given")} ' if author.get("given") else ""
            author_name += f'{author.get("family")} ' if author.get("family") else ""
            author_name = author_name.strip()

            if author.get("sequence") == "first":
                main_author = author_name
            else:
                other_authors.append(author_name)

        # get title
        title = data.get("title")
        if title:
            title = title[0]
            title = title.strip().strip(".")
        else:
            msg = f"Failed to extract title from 'title' key: {title}."
            raise cls.Exceptions.CrossrefException(msg)

        # get subtitle
        subtitle = data.get("subtitle")
        if subtitle:
            subtitle = subtitle[0]
        else:
            subtitle = None

        # get journal title and subtitle
        container = data.get("container-title")  # type: ignore
        if container:
            container: str = container[0]
        else:
            msg = f"Failed to get container from 'container-title' key: {container}."
        try:
            journal_title, journal_subtitle = container.split(":", 1)
            journal_title.strip().strip(".")
            journal_subtitle = journal_subtitle.strip().strip(".")
        except ValueError:
            journal_title = container
            journal_subtitle = None

        # get doi
        doi = data.get("DOI")
        if not doi:
            msg = f"Failed to get DOI."
            raise cls.Exceptions.CrossrefException(msg)

        # get url
        link = data.get("link")
        if link:
            url = link[0].get("URL")
        else:
            msg = f"Failed to get work url from 'link' key: {link}."
            raise cls.Exceptions.CrossrefException(msg)

        # get location
        location = data.get("publisher-location")
        if not location:
            location = "[S.l.]"

        # get volume
        volume = data.get("volume")
        if volume:
            volume = int(volume)

        # get issue number
        issue = data.get("issue")
        if issue:
            issue = int(issue)

        # TODO: get section

        # get pages
        pages = data.get("page")  # type: ignore
        if not pages:
            msg = f"Failed get page number from 'page' key: {pages}."
            raise cls.Exceptions.CrossrefException(msg)

        # get publish date
        try:
            published_date_parts = data.get("published").get("date-parts")[0]  # type: ignore
        except Exception as e:
            msg = f"Failed to extract date parts from 'published' key: {e.__class__.__name__}: {e}."
            raise cls.Exceptions.CrossrefException(msg)

        year, month, day = published_date_parts
        published_at = date(year=year, month=month, day=day)

        return JournalArticle(
            main_author=main_author,
            other_authors=other_authors,
            title=title,
            subtitle=subtitle,
            journal_title=journal_title,
            journal_subtitle=journal_subtitle,
            doi=doi,
            url=url,
            location=location,
            volume=volume,
            issue=issue,
            pages=pages,
            published_at=published_at,
        )

    @classmethod
    async def get_from_doi(cls, doi: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.crossref.org/works/{doi}") as work_res:
                if work_res.status != 200:
                    msg = f"Unexpected status code when requestion work metadat from crossref: {work_res.status}."
                    raise cls.Exceptions.CrossrefException(msg)

                work_res = await work_res.json()

        work_type = work_res.get("message").get("type")
        match work_type:
            case CrossrefTypes.journal_article.value:
                return cls._format_journal_article(work_res)

            case _:
                return work_res

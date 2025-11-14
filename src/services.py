import json
from enum import Enum
from datetime import date
from urllib.parse import urljoin
import asyncio
import re

import aiohttp

from .schemas import JournalArticle, ProceedingsArticle, Monograph


class CrossrefTypes(Enum):
    journal_article = "journal-article"
    proceedings_article = "proceedings-article"


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
            # skip non fisical peson authors
            if author.get("name"):
                continue

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
            subtitle = subtitle.strip().strip(".")
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
            journal_title = journal_title.strip().strip(".")
            journal_subtitle = journal_subtitle.strip().strip(".")
        except ValueError:
            journal_title = container.strip().strip(".")
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
            url = data.get("URL")
        if not url:
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
        # if not pages:
        #     msg = f"Failed get page number from 'page' key: {pages}."
        #     raise cls.Exceptions.CrossrefException(msg)

        # get publish date
        try:
            try:
                published_date_parts = data.get("published").get("date-parts")[0]  # type: ignore
            except AttributeError:
                published_date_parts = data.get("created").get("date-parts")[0]  # type: ignore
        except Exception as e:
            msg = f"Failed to extract date parts from 'published' key: {e.__class__.__name__}: {e}."
            raise cls.Exceptions.CrossrefException(msg)

        try:
            year, month, day = published_date_parts
            published_at = date(year=year, month=month, day=day)
        except ValueError:
            published_at = published_date_parts[0]

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
    def _format_proceedings_article(cls, data: dict):
        data = data.get("message")  # type: ignore

        # get author names
        authors = data.get("author")
        main_author = ""
        other_authors = []
        for author in authors:  # type: ignore
            # skip non fisical peson authors
            if author.get("name"):
                continue

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
            subtitle = subtitle.strip().strip(".")
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
            journal_title = journal_title.strip().strip(".")
            journal_subtitle = journal_subtitle.strip().strip(".")
        except ValueError:
            journal_title = container.strip().strip(".")
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
            url = data.get("URL")
        if not url:
            msg = f"Failed to get work url from 'link' key: {link}."
            raise cls.Exceptions.CrossrefException(msg)

        # get location
        location = data.get("event")
        if location:
            location = location.get("location")
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

        # get pages
        pages = data.get("page")  # type: ignore
        # if not pages:
        #     msg = f"Failed get page number from 'page' key: {pages}."
        #     raise cls.Exceptions.CrossrefException(msg)

        # get publish date
        try:
            try:
                published_date_parts = data.get("published").get("date-parts")[0]  # type: ignore
            except AttributeError:
                published_date_parts = data.get("created").get("date-parts")[0]  # type: ignore
        except Exception as e:
            msg = f"Failed to extract date parts from 'published' key: {e.__class__.__name__}: {e}."
            raise cls.Exceptions.CrossrefException(msg)

        try:
            year, month, day = published_date_parts
            published_at = date(year=year, month=month, day=day)
        except ValueError:
            published_at = published_date_parts[0]

        return ProceedingsArticle(
            main_author=main_author,
            other_authors=other_authors,
            title=title,
            subtitle=subtitle,
            proceeding_title=journal_title,
            proceeding_subtitle=journal_subtitle,
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

                # open("dbg/output.json", "w", encoding="utf8").write(json.dumps(work_res, indent=2))

        work_type = work_res.get("message").get("type")
        match work_type:
            case CrossrefTypes.journal_article.value:
                return cls._format_journal_article(work_res)

            case CrossrefTypes.proceedings_article.value:
                return cls._format_proceedings_article(work_res)

            case _:
                msg = f"Work type not implemented yet: {work_type}."
                raise cls.Exceptions.CrossrefException(msg)


class OpenlibraryService:
    class Exceptions:
        class OpenlibraryException(Exception):
            pass

    @classmethod
    def _format_monograph(cls, data: dict, isbn: str):
        # get url
        url = data.get(f"ISBN:{isbn}").get("info_url")  # type: ignore

        # update data
        data = data.get(f"ISBN:{isbn}").get("details")  # type: ignore

        # get authors
        main_author = ""
        other_authors = []
        if data.get("authors") and data.get("authors")[0].get("name") != "[author not identified]":  # type: ignore
            for i, author in enumerate(data.get("authors")):  # type: ignore
                name = author.get("name")
                if i == 0:
                    main_author = name
                else:
                    other_authors.append(name)

        # use publisher name when authors are omited
        else:
            for i, name in enumerate(data.get("publishers")):  # type: ignore
                if i == 0:
                    main_author = name
                else:
                    other_authors.append(name)

        # get title and subtitle
        title = data.get("title")
        subtitle = data.get("subtitle")

        # get publisher
        publisher = data.get("publishers")[0]  # type: ignore

        # get published year
        published_at = int(re.search(r"\d{4}", data.get("publish_date")).group())  # type: ignore

        # get revision
        edition = int(data.get("revision")) if data.get("revision") else None  # type: ignore

        # get location
        location = data.get("publish_places")[0] if data.get("publish_places") else "[S.l.]"  # type: ignore

        return Monograph(
            main_author=main_author,
            other_authors=other_authors,
            title=title,  # type: ignore
            subtitle=subtitle,
            isbn=isbn,
            url=url,
            publisher=publisher,
            edition=edition,
            location=location,
            published_at=published_at,
        )

    @classmethod
    async def get_from_isbn(cls, isbn: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=details&format=json") as book_res:
                if book_res.status != 200:
                    msg = f"Unexpected status code when requestion work metadat from crossref: {book_res.status}."
                    raise cls.Exceptions.OpenlibraryException(msg)

                book_res = await book_res.json()

            # open("dbg/output.json", "w", encoding="utf8").write(json.dumps(book_res, indent=2))

            return cls._format_monograph(book_res, isbn)

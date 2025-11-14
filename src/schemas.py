from datetime import date

from typing import Optional

from pydantic import BaseModel


class JournalArticle(BaseModel):
    main_author: str
    other_authors: Optional[list[str]] = []

    title: str
    subtitle: Optional[str] = None

    journal_title: str
    journal_subtitle: Optional[str] = None

    doi: Optional[str] = None
    url: Optional[str] = None

    location: Optional[str] = "[S.l.]"
    volume: Optional[int] = None
    issue: Optional[int] = None
    section: Optional[str] = None
    pages: Optional[str] = None

    published_at: date | int


class ProceedingsArticle(BaseModel):
    main_author: str
    other_authors: Optional[list[str]] = []

    title: str
    subtitle: Optional[str] = None

    proceeding_title: str
    proceeding_subtitle: Optional[str] = None

    doi: Optional[str] = None
    url: Optional[str] = None

    location: Optional[str] = "[S.l.]"
    volume: Optional[int] = None
    issue: Optional[int] = None
    section: Optional[str] = None
    pages: Optional[str] = None

    published_at: date | int


class Monograph(BaseModel):
    main_author: str
    other_authors: Optional[list[str]] = []

    title: str
    subtitle: Optional[str] = None

    isbn: Optional[str] = None
    url: Optional[str] = None

    edition: Optional[int] = None
    publisher: str
    location: Optional[str] = "[S.l.]"

    published_at: int

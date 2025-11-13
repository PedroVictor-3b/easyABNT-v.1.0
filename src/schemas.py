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
    pages: str

    published_at: date

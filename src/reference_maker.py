from datetime import date

from .schemas import JournalArticle, ProceedingsArticle, Monograph
import isbnlib

month_map = {
    1: "jan.",
    2: "fev.",
    3: "mar.",
    4: "abr.",
    5: "maio",
    6: "jun.",
    7: "jul.",
    8: "ago.",
    9: "set.",
    10: "out.",
    11: "nov.",
    12: "dez.",
}


# ABNT NBR 6023:2025 - 7.1.1; 7.2.1; 7.2.2
def format_monograph(data: Monograph):
    # format author names
    author_names = data.main_author.split(" ")
    author_str = f"{author_names.pop().upper()}, {' '.join(author_names)}"
    for author in data.other_authors:  # type: ignore
        author_names = author.split(" ")
        author_str += f"; {author_names.pop().upper()}, {' '.join(author_names)}"

    # basic required reference data
    title_str = f"<strong>{data.title}</strong>: {data.subtitle}" if data.subtitle else f"<strong>{data.title}</strong>"
    edition_str = f"{data.edition}. ed. " if data.edition else ""
    location_str = f"{data.location}: {data.publisher}, {data.published_at}"

    # format reference
    reference = f"{author_str}. {title_str}. {edition_str}{location_str}. <i>E-book</i>."

    # remove double dots from abbreviated names
    reference = reference.replace("..", ".")

    # add isbn
    isbn_str = f" ISBN: {isbnlib.mask(data.isbn)}." if data.isbn else ""
    reference += isbn_str

    # add online access required data
    today = date.today()
    online_access_str = f" Disponível em: {data.url}. Acesso em: {today.day} {month_map[today.month]} {today.year}." if data.url else ""
    reference += online_access_str

    return reference


# ABNT NBR 6023:2025 - 7.7.5; 7.7.6
def format_proceedings_artice(data: ProceedingsArticle):
    # format author names
    author_names = data.main_author.split(" ")
    author_str = f"{author_names.pop().upper()}, {' '.join(author_names)}"
    for author in data.other_authors:  # type: ignore
        author_names = author.split(" ")
        author_str += f"; {author_names.pop().upper()}, {' '.join(author_names)}"

    # basic required reference data
    title_str = f"{data.title}: {data.subtitle}" if data.subtitle else data.title
    journal_title_str = f"<strong>{data.proceeding_title}</strong>: {data.proceeding_subtitle}" if data.proceeding_subtitle else f"<strong>{data.proceeding_title}</strong>"
    volume_str = f", v. {data.volume}" if data.volume else ""
    issue_str = f", n. {data.issue}" if data.issue else ""
    date_str = f", {data.published_at.year}" if isinstance(data.published_at, date) else f", {data.published_at}"
    page_str = f", p. {data.pages}" if data.pages else ""

    # format reference data
    reference = f"{author_str}. {title_str}. {journal_title_str}, {data.location}{volume_str}{issue_str}{page_str}{date_str}."

    # remove double dots from abbreviated names
    reference = reference.replace("..", ".")

    # add doi
    doi_str = f" DOI: {data.doi}." if data.doi else ""
    reference += doi_str

    # add online access required data
    today = date.today()
    online_access_str = f" Disponível em: {data.url}. Acesso em: {today.day} {month_map[today.month]} {today.year}." if data.url else ""
    reference += online_access_str

    return reference


# ABNT NBR 6023:2025 - 7.7.7; 7.7.8
def format_journal_artice(data: JournalArticle):
    # format author names
    author_names = data.main_author.split(" ")
    author_str = f"{author_names.pop().upper()}, {' '.join(author_names)}"
    for author in data.other_authors:  # type: ignore
        author_names = author.split(" ")
        author_str += f"; {author_names.pop().upper()}, {' '.join(author_names)}"

    # basic required reference data
    title_str = f"{data.title}: {data.subtitle}" if data.subtitle else data.title
    journal_title_str = f"<strong>{data.journal_title}</strong>: {data.journal_subtitle}" if data.journal_subtitle else f"<strong>{data.journal_title}</strong>"
    volume_str = f", v. {data.volume}" if data.volume else ""
    issue_str = f", n. {data.issue}" if data.issue else ""
    section_str = f", {data.section}, p. {data.pages}" if data.section else ""
    date_str = f", {data.published_at.year}" if isinstance(data.published_at, date) else f", {data.published_at}"
    page_str = f", p. {data.pages}" if data.pages else ""

    # variable required reference data
    reference = f"{author_str}. {title_str}. {journal_title_str}, {data.location}{volume_str}{issue_str}"
    reference_ending_str = f"{date_str}. {section_str}." if section_str else f"{page_str}{date_str}."
    reference += reference_ending_str

    # remove double dots from abbreviated names
    reference = reference.replace("..", ".")

    # add doi
    doi_str = f" DOI: {data.doi}." if data.doi else ""
    reference += doi_str

    # add online access required data
    today = date.today()
    online_access_str = f" Disponível em: {data.url}. Acesso em: {today.day} {month_map[today.month]} {today.year}." if data.url else ""
    reference += online_access_str

    return reference

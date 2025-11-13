import asyncio


async def main():
    import json
    from pprint import pprint
    from src.services import CrossrefService
    from src.reference_maker import format_journal_artice, format_proceedings_artice
    from src.schemas import JournalArticle, ProceedingsArticle

    res = await CrossrefService.get_from_doi("10.18844/gjcs.v12i1.7449")
    if isinstance(res, dict):
        open("dbg/output.json", "w", encoding="utf8").write(json.dumps(res, indent=2))

    elif isinstance(res, JournalArticle):
        print(format_journal_artice(res))

    elif isinstance(res, ProceedingsArticle):
        print(format_proceedings_artice(res))


if __name__ == "__main__":
    asyncio.run(main())

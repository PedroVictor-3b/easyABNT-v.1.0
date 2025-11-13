import asyncio


async def main():
    import sys
    import json
    from src.services import CrossrefService, OpenlibraryService
    from src.reference_maker import format_journal_artice, format_proceedings_artice, format_monograph
    from src.schemas import JournalArticle, ProceedingsArticle, Monograph

    match sys.argv[1]:
        case "doi":
            res = await CrossrefService.get_from_doi(sys.argv[2])
            if isinstance(res, dict):
                open("dbg/output.json", "w", encoding="utf8").write(json.dumps(res, indent=2))

            elif isinstance(res, JournalArticle):
                print(format_journal_artice(res))

            elif isinstance(res, ProceedingsArticle):
                print(format_proceedings_artice(res))

        case "isbn":
            res = await OpenlibraryService.get_from_isbn(sys.argv[2])
            if isinstance(res, dict):
                open("dbg/output.json", "w", encoding="utf8").write(json.dumps(res, indent=2))
            if isinstance(res, Monograph):
                print(format_monograph(res))


if __name__ == "__main__":
    asyncio.run(main())

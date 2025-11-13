import asyncio


async def main():
    import json
    from pprint import pprint
    from src.services import CrossrefService
    from src.reference_maker import format_journal_artice

    res = await CrossrefService.get_from_doi("10.11648/j.mlr.20251001.12")
    if isinstance(res, dict):
        open("dbg/output.json", "w", encoding="utf8").write(json.dumps(res, indent=2))
        return

    print(format_journal_artice(res))


if __name__ == "__main__":
    asyncio.run(main())

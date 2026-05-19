import typing

TAGS: list[dict[str, str]] = []


def add_tags(result: dict[str, typing.Any], **kwargs: typing.Any) -> dict[str, typing.Any]:
    result.setdefault("tags", [])
    existing = {t["name"] for t in result["tags"]}
    result["tags"] += [t for t in TAGS if t["name"] not in existing]
    return result

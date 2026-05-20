import json
import typing

from django.core.management.base import BaseCommand
from django.urls import get_resolver


class Command(BaseCommand):
    help = "Export top-level URL prefixes as a web-server-agnostic JSON array."

    def add_arguments(self, parser: typing.Any) -> None:
        parser.add_argument(
            "--output",
            "-o",
            type=str,
            default=None,
            help="Output file path. Defaults to stdout.",
        )

    def handle(self, *args: typing.Any, **options: typing.Any) -> None:
        prefixes: set[str] = set()
        for pattern in get_resolver().url_patterns:
            segment = str(pattern.pattern).lstrip("^").split("/")[0]
            if segment:
                prefixes.add(segment)

        output = json.dumps(sorted(prefixes), indent=2)

        if options["output"]:
            with open(options["output"], "w") as f:
                f.write(output)
                f.write("\n")
            self.stdout.write(f"URL prefixes written to {options['output']}")
        else:
            self.stdout.write(output)

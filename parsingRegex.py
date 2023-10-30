from RegexParser import RegexParser, regex1, regex2
from typing import Any
import json

from interfaces import CiaDataFileSchema


class ParserClient:
    result: list[dict[str, Any]] = []
    regex_parser = RegexParser()
    patterns = [regex1, regex2, r"(English)$"]

    def __init__(self, data: list[CiaDataFileSchema]):
        self.data = data

    def save_as_text(self, data: Any):
        with open(self.save_location, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Saved to {self.save_location}")

    def parse_language_info(self):
        passed_results: dict[str, dict[str, Any]] = {}
        failed_results: dict[str, str] = {}

        for info in self.data:
            # Search for % and the reference of it inside the info
            result: dict[str, str] | None = None
            for pattern in self.patterns:
                result = self.regex_parser.parse(info.languageInfo, pattern)
                if result is not None:
                    passed_results[info.heading] = result
                    break

            if result is None:
                failed_results[info.heading] = info.languageInfo

        self.save_location = "zsucceeded.json"
        self.save_as_text(passed_results)

        self.save_location = "zfailed.json"
        self.save_as_text(failed_results)

    def print_results(self):
        print(self.result)


def main():
    with open("ciaData.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    validated_initial_data: list[CiaDataFileSchema] = [
        CiaDataFileSchema(**data) for data in data
    ]
    parser = ParserClient(validated_initial_data)
    parser.parse_language_info()


main()

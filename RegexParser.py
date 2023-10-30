import re

pattern = r"([^\d<%]+) (\d+\.\d+%|\d+%)(?!(\s<\d+%))"
RegexResult = list[list[str]]
ReturnedResult = dict[str, str]  # A dict of languages and their percentages
regex1 = r"([^\d<%]+) (\d+\.\d+%|\d+%)(?!(\s<\d+%))"
regex2 = r"^(\w+) \(official"  # should capture English in "English (official),"


class RegexParser:
    def parse(self, data: str, pattern: str) -> ReturnedResult | None:
        matched_result: RegexResult = re.findall(pattern, data)
        if len(matched_result) == 0:
            return None
        language_data_set: dict[str, str] = {}

        for match in matched_result:
            language_spoken = match[0].replace(", ", " ").strip()
            percentage = match[1]

            language_data_set[language_spoken] = percentage
        
        return language_data_set

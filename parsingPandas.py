import re
from RegexParser import regex1, regex2
import json
from typing import Any
import pandas as pd

deeplSuppoortedLanguages = [
    "Bulgarian",
    "Czech",
    "Danish",
    "German",
    "Greek",
    "English",
    "Spanish",
    "Estonian",
    "Finnish",
    "French",
    "Hungarian",
    "Indonesian",
    "Italian",
    "Japanese",
    "Korean",
    "Lithuanian",
    "Latvian",
    "Norwegian",
    "Dutch",
    "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Slovak",
    "Slovenian",
    "Swedish",
    "Turkish",
    "Ukrainian",
    "Chinese",
]


class UsingPandas:
    patterns = [regex1, regex2, r"(English)$"]

    def __init__(self, data: dict[str, str]):
        self.data = data

    def save_as_text(self, data: dict[str, str]):
        with open(self.save_location, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Saved to {self.save_location}")  # type: ignore

    def extract_language(self, lang: str):
        words = re.findall(r"\b\w+\b", lang)
        for word in words:
            if word in deeplSuppoortedLanguages:
                return word
        return lang

    def parsingPandas(self):
        df = pd.DataFrame(columns=["Country", "LangInfo"])
        for value in self.data:
            df = df._append(  # type: ignore
                {"Country": value["heading"], "LangInfo": self.extract_language(value["languageInfo"])},  # type: ignore
                ignore_index=True,
            )  # type: ignore

        lang: Any
        count = 0
        for lang in df["LangInfo"]:
            for pattern in self.patterns:
                result = re.search(pattern, lang)
                if result:
                    df["LangInfo"] = df["LangInfo"].str.replace(" ", "")  # type: ignore
                    df["LangInfo"] = df["LangInfo"].str.replace(".", "")  # type: ignore
                    df["LangInfo"] = df["LangInfo"].str.replace(",", "")  # type: ignore
                    df["LangInfo"] = df["LangInfo"].str.replace(r"\d+%", "", regex=True)  # type: ignore
                    df["LangInfo"] = df["LangInfo"].str.replace("(official", "")  # type: ignore
                    df["LangInfo"].iloc[count] = result.group(0)  # type: ignore
            count += 1
        self.save_location = "file.json"
        data_dict = df.set_index("Country")["LangInfo"].to_dict()  # type: ignore
        self.save_as_text(data_dict)  # type: ignore


def main():
    with open("ciaData.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    panda = UsingPandas(data)
    panda.parsingPandas()


main()

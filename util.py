from dataclasses import dataclass
import json
import re
from typing import Any, TypedDict
import pandas as pd

from RegexParser import ReturnedResult
from interfaces import OriginalCiaLanguageData

class CheckReturnResult(TypedDict):
    CountryData1: str
    CountryData2: str
    Result: bool
    Similarity: int
    Similarities: dict[str, int]

def clean_wiki_data(wikiData:list[dict[str,str]]):
    
    for wikiCountry in wikiData:
        result_string = re.sub(r"\d+", "", wikiCountry["Country/Region"])
        result_string = result_string.replace("[", "")
        result_string = result_string.replace("]", "")
        wikiCountry["Country/Region"] = result_string
    return wikiData


def init_df(results:list[ReturnedResult]):
    df = pd.DataFrame(results)
    return df
from __future__ import annotations
from dataclasses import dataclass
import json
from typing import TypedDict
import pandas as pd
import re
from pyparsing import Any

from thefuzz import fuzz # type: ignore


class Matching:
    def __init__(self, wiki: dict[str, str], cia: dict[str, str]):
        self.cia = cia
        self.wiki = wiki

    

    # takes a country to compare and a list of countries and return object with most similar country
    def check(self, country_to_compare: str, country_list: list[str]):
        
        
        
        
        most_similar = 0
        similarities = {}
        most_similar_country = None
        for country_item in country_list:
            # get similarity (ratio seems the best here but idk)
            similarity = fuzz.ratio(country_to_compare, country_item)

            if similarity == 100:
                return CheckReturnResult(**{
                    "CountryData1": country_to_compare,
                    "CountryData2": country_item,
                    "Result": True,
                    "Similarity": similarity,
                    "Similarities": {None},
                })

            # replace if the current country is more similar than the prev one
            if similarity > most_similar:
                most_similar = similarity
                most_similar_country = country_item

            # if similarity between 40 and 90%, add to list of similarities
            if similarity > 40:
                similarities[f"{country_item}"] = similarity

            
            
        return CheckReturnResult(**{
            "CountryData1": country_to_compare,
            "CountryData2": most_similar_country,
            "Result": False,
            "Similarity": most_similar,
            "Similarities": similarities,
        })
        

class CheckReturnResult(TypedDict):
    CountryData1: str
    CountryData2: str
    Result: bool
    Similarity: int
    Similarities: dict[str, int]


def getWikiData(wikiData:Any) -> list[str]:
    wikiCountryList = []
    for wikiCountry in wikiData:
        result_string = re.sub(r"\d+", "", wikiCountry["Country/Region"])
        result_string = result_string.replace("[", "")
        result_string = result_string.replace("]", "")
        wikiCountryList.append(result_string)
    return wikiCountryList


def get_results():
    with open("file.json", "r", encoding="utf-8") as f:
        ciaFinalData:dict[str,str] = json.load(f)
    with open("wikiData.json", "r", encoding="utf-8") as f:
        wikiData:dict = json.load(f)

    matching = Matching(wikiData, ciaFinalData)

    # make a parsed list of countries with wiki data

    # compare each country from cia to each country in wikiCountryList

    cleaned_country_string = list(map(lambda key: key.replace(",",""), ciaFinalData.keys()))

    results = [
        matching.check(cleaned_country, getWikiData(wikiData))
        for cleaned_country in cleaned_country_string
    ]
    return results




def main():
    results = get_results()
    
    
    
    
            
    

    df = pd.DataFrame(results)
    df.to_csv("partial_token_sort_ratio.csv", index=False)


main()

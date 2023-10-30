from __future__ import annotations
import re
from typing import TypeVar, TypedDict



T = TypeVar("T")

def create_data_file_schema_from_dict(data:dict[str,str]) -> list[CiaDataFileSchema]:
    result:list[CiaDataFileSchema] = []
    for key, value in data.items():
        result.append(CiaDataFileSchema(heading=key, languageInfo=value))
    return result


class CiaDataFileSchema(TypedDict):
    heading: str
    languageInfo: str
    
    
        


class CiaFullData(TypedDict):
    country: str
    languages: dict[str, str]


class CiaData(TypedDict):
    primary_language: str  
    full_data: CiaFullData


class WikipediaFullData(TypedDict):
    widely_spoken: str
    country_or_region: str
    minority_language: str
    national_language: str
    official_language: str
    regional_language: str

        

class WikipediaData(TypedDict):
    primary_language: str 
    full_data: WikipediaFullData


class CountryResult(TypedDict): 
    country_name: str
    cia_data: CiaData
    wikipedia_data: WikipediaData






class InnerPdData(TypedDict):
    compared_country_id: int
    common_score: int
    common_score_token_set: int
    common_country: str
    compared_country: str
    official_score: int
    official_score_token_set: int
    official_country: str


class OriginalCiaLanguageData(TypedDict):
    heading: str
    languageInfo: dict[str, str]
    

class LangNameData(TypedDict):
    id: int
    common: str
    official: str
    nativeName: dict

class NewCiaData(TypedDict):
    country:str
    primary_language:str

def create_new_cia_data_from_file_schema(data:list[CiaDataFileSchema]) -> list[NewCiaData]:
    result:list[NewCiaData] = []
    for item in data:
        result.append(NewCiaData(country=item["heading"], primary_language=item["languageInfo"]))
    return result


class BaseDfStruct(TypedDict):
    cia_country:str
    wiki_country:str
    
    
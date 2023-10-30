import json
from Matching import Matching

from interfaces import BaseDfStruct, CiaDataFileSchema, LangNameData, NewCiaData, OriginalCiaLanguageData, WikipediaFullData, create_data_file_schema_from_dict, create_new_cia_data_from_file_schema
from matchingCIAandWiki import get_results
from util import clean_wiki_data


class FileService:
    
    cia_path = "file.json"
    wiki_path = "wikiData.json"
    clean_wiki_path = "wikiDataClean.json"
    lang_path = "langNames.json"
    original_cia_path = "ciaData.json"
    
    def get_new_cia_files(self):
        with open(self.cia_path, "r", encoding="utf-8") as f:
            ciaFinalData: dict[str, str] = json.load(f)
        return create_new_cia_data_from_file_schema( create_data_file_schema_from_dict(ciaFinalData))


 
    def get_wikiData_file_data(self):
        with open(self.clean_wiki_path, "r", encoding="utf-8") as f:
            wiki_data:list[dict[str,str]] = json.load(f)
            

        return [WikipediaFullData(**item) for item in wiki_data]
        

    def get_lang_files(self):
        with open(self.lang_path, "r", encoding="utf-8") as f:
            langNames: list[dict] = json.load(f)

        return [LangNameData(**item) for item in langNames]
 


def getFiles():
    with open("file.json", "r", encoding="utf-8") as f:
        ciaFinalData: dict[str, str] = json.load(f)
    with open("wikiData.json", "r", encoding="utf-8") as f:
        wikiData: dict = json.load(f)
    return {"wiki": wikiData, "cia": ciaFinalData}


def get_new_cia_files():
    with open("file.json", "r", encoding="utf-8") as f:
        ciaFinalData: dict[str, str] = json.load(f)
    return ciaFinalData


def get_wiki_files():
    with open("wikiData.json", "r", encoding="utf-8") as f:
        wikiData:list[dict[str,str]] = json.load(f)
    return clean_wiki_data(wikiData)
    


def getLangFiles():
    with open("langNames.json", "r", encoding="utf-8") as f:
        langNames: list[LangNameData] = json.load(f)

    return langNames


def get_original_lang_files():
    with open("ciaData.json", "r", encoding="utf-8") as f:
        cia_original_lang_data: list[OriginalCiaLanguageData] = json.load(f)

    return cia_original_lang_data

# def create_data_for_new_cia_df() -> list[NewCiaData]:
#     res = get_new_cia_files().items()
    
#     return [
#         NewCiaData(
#             {"country": item[0], "primary_language": item[1]}
#         )
#         for item in res
#     ]
    
    

# def create_data_for_base_df() -> list[BaseDfStruct]:
#     res = get_results()
    
    
#     return [
#         BaseDfStruct(
#             {"cia_country": item["CountryData1"], "wiki_country": item["CountryData2"]}
#         )
#         for item in res
#     ]

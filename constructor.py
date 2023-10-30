


from typing import TypedDict
from pandas import DataFrame
from file_service import FileService
from interfaces import BaseDfStruct, CiaDataFileSchema, LangNameData, NewCiaData, OriginalCiaLanguageData, WikipediaData, WikipediaFullData
from matchingCIAandWiki import getWikiData

class CreateBaseDfReturn(TypedDict):
    base_df: DataFrame
    df: DataFrame


class DataframeConstructor:
    file_service = FileService()
    
    
    def create_base_df(self, results:list[BaseDfStruct]) -> CreateBaseDfReturn:
        
        
        base_df = DataFrame(results)
        df = base_df.copy()
        
        return_result: CreateBaseDfReturn = {
            "base_df": base_df,
            "df": df
        }
        return return_result
    
    
        
        
    def create_rest_api_language_name_dataframe(self):
        return DataFrame(self.file_service.get_lang_files())
        
    
    
    
    def create_new_cia_language_dataframe(self):
        
        return DataFrame(self.file_service.get_new_cia_files())
    
    def create_wiki_language_df(self):
        return DataFrame(self.file_service.get_wikiData_file_data())
    
import json
from FuzzySearcher import FuzzySearcher
from matchingCIAandWiki import getWikiData
from util import CheckReturnResult





class Matching:
    
    def __init__(self, wiki: dict[str, str], cia: dict[str, str], searcher = FuzzySearcher()):
        self.cia = cia
        self.wiki = wiki
        self.searcher=searcher

    

    # takes a country to compare and a list of countries and return object with most similar country
    def _check(self, country_to_compare: str, country_list: list[str]):
        
        
        
        
        most_similar = 0
        similarities = {}
        most_similar_country = None
        for country_item in country_list:
            # get similarity (ratio seems the best here but idk)
            similarity = self.searcher.run(country_to_compare, country_item)

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
        
    def getResults(self):
            country_string = self.cia.keys()
            # cleaned_country_string = list(map(lambda key: key.replace(",",""), self.cia.keys()))
            return [
                self._check(cleaned_country, getWikiData(self.wiki))
                for cleaned_country in country_string
            ]
        


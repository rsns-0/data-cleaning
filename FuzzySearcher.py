
from dataclasses import dataclass
from typing import Literal, TypedDict
from pandas import DataFrame
from pydantic import BaseModel


from thefuzz import fuzz

Strategies = Literal["ratio","partial_ratio","token_sort_ratio","token_set_ratio"]


class FuzzySearcherResult(BaseModel):
    right:str
    similarity:int
    strategy:Strategies


class FuzzySearcherData(BaseModel):
    left: str
    data: list[FuzzySearcherResult]
    top_result: FuzzySearcherResult
    
    @staticmethod
    def create(left:str, data:list[FuzzySearcherResult]):
        top_result = max(data, key=lambda x: x.similarity)
        return FuzzySearcherData(
            left=left,
            data=data,
            top_result=top_result
        )


    
    
        

class FuzzySearcher:
    
    def __init__(self, strategy:Strategies = "ratio"):
        self.strategy:Strategies = strategy
    
    def run(self, left: str, right: str):
        match self.strategy:
            case "ratio":
                return fuzz.ratio(left, right)
            case "partial_ratio":
                return fuzz.partial_ratio(left, right)
            case "token_sort_ratio":
                return fuzz.token_sort_ratio(left, right)
            case "token_set_ratio":
                return fuzz.token_set_ratio(left, right)
            case _:
                raise NotImplementedError
    
    def run_against_multiple_impl(self, string:str, other_list:list[str]):
        results:list[FuzzySearcherResult] = []
        for country_item in other_list:
            similarity = self.run(string, country_item)
            results.append(FuzzySearcherResult(right=country_item, similarity=similarity, strategy=self.strategy))
        return results
    
    def run_against_multiple(self, string:str, other_list:list[str]):
        
        results = self.run_against_multiple_impl(string, other_list)
        
        return FuzzySearcherData.create(string, results)


class AggregateFuzzySearcher:
    
    searchers:list[FuzzySearcher]
    
    def __init__(self, searchers:list[FuzzySearcher]):
        self.searchers = searchers
    
    @staticmethod
    def create(searchers:list[Strategies]):
        return AggregateFuzzySearcher([FuzzySearcher(strategy=strategy) for strategy in searchers])
    
    
    def run_against_multiple(self, string:str, other_list:list[str]):
        results:list[FuzzySearcherResult] = []
        for searcher in self.searchers:
            result = searcher.run_against_multiple_impl(string, other_list)
            results.extend(result)
            
        return FuzzySearcherData.create(string, results)
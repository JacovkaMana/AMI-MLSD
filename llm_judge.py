from llm import LLM
from loguru import logger
import os
from dotenv import load_dotenv
import json

load_dotenv()


class LLMJudge:
    def __init__(self):
        self.llm = LLM(
            temperature=0.2,
            response_format="json_object",
            system_prompt="""
You are an evaluation assistant. 
Your task is to evaluate the relevance and creativity of a given response to a query. 
For relevance, provide a numerical score from 1 to 100, where 1 is low relevance and 100 is high relevance and an explanation. 
For creativity, provide a brief explanation.""",
        )

    def evaluate(self, query, result):
        relevance_prompt = f"""
Given the query: '{query}', evaluate the relevance of the result: '{result}'. 
Provide a numerical score from 1 to 100, where 1 is low relevance and 100 is high relevance and an explanation.
Return json 

{{
    'score' : int
    'explanation' : str
}}"""
        relevance_response = json.loads(self.llm.complete(relevance_prompt))
        creativity_prompt = f"""
Given the query: '{query}', evaluate the creativity of the result: '{result}'. 
Provide a numerical score from 1 to 100, where 1 is low creativity and 100 is high creativity and an explanation.
Return json 

{{
    'score' : int
    'explanation' : str
}}"""
        creativity_response = json.loads(self.llm.complete(creativity_prompt))

        return relevance_response, creativity_response


if __name__ == "__main__":
    query = "Create a fantasy world..."
    result = "A medieval kingdom with forests and mountains."
    judge = LLMJudge()
    evaluation = judge.evaluate(query, result)
    logger.info(f"Evaluation: {evaluation}")

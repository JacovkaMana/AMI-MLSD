from llm import LLM
from loguru import logger
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from pathlib import Path
from rouge_judge import RougeLJudge

load_dotenv()


class BaseJudge:
    def __init__(self, metric_name, system_prompt):
        self.metric_name = metric_name
        self.llm = LLM(
            temperature=0.2,
            response_format="json_object",
            system_prompt=system_prompt,
            model_name="mistral-small-latest",
        )

    def evaluate(self, query, result):
        prompt = f"""
Given the query: '{query}', evaluate the {self.metric_name} of: '{result}'.
Provide a numerical score (1-100) and explanation.
Return json format:
{{
    'score': int,
    'explanation': str
}}"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.llm.complete(prompt)
                return json.loads(response)
            except json.JSONDecodeError as e:
                logger.warning(
                    f"Attempt {attempt + 1} failed to parse JSON response: {e}"
                )
                if attempt == max_retries - 1:
                    raise ValueError(
                        f"Failed to get valid JSON after {max_retries} attempts"
                    )
                continue


class RelevanceJudge(BaseJudge):
    def __init__(self):
        super().__init__(
            "relevance", "Evaluate how well the response matches the query (1-100)."
        )


class CreativityJudge(BaseJudge):
    def __init__(self):
        super().__init__("creativity", "Evaluate originality and novelty (1-100).")


class CompletenessJudge(BaseJudge):
    def __init__(self):
        super().__init__("completeness", "Evaluate coverage of key aspects (1-100).")


class EngagementJudge(BaseJudge):
    def __init__(self):
        super().__init__("engagement", "Evaluate how compelling/interesting (1-100).")


class ClarityJudge(BaseJudge):
    def __init__(self):
        super().__init__("clarity", "Evaluate how clear and understandable (1-100).")


class Evaluator:
    def __init__(self):
        self.judges = {
            "relevance": RelevanceJudge(),
            "creativity": CreativityJudge(),
            "completeness": CompletenessJudge(),
            "engagement": EngagementJudge(),
            "clarity": ClarityJudge(),
            "rouge_l": RougeLJudge(),
        }

    def evaluate(self, query, result, reference_dataset=None):
        evaluations = {}
        for name, judge in self.judges.items():
            if name == "rouge_l":
                evaluation = judge.evaluate(query, result, reference_dataset)
            else:
                evaluation = judge.evaluate(query, result)
            evaluations[name] = evaluation
        return evaluations


if __name__ == "__main__":
    # Simple test case
    evaluator = Evaluator()
    test_eval = evaluator.evaluate("Test query", "Test result")
    logger.info(f"Test evaluation: {test_eval}")

import os
from dotenv import load_dotenv
from loguru import logger


def tokenise(text):
    """Tokenize text into words for ROUGE calculation."""
    return text.split()


def longest_common_subsequence(A, B):
    """Compute the length of the longest common subsequence between two lists of words."""
    m = len(A)
    n = len(B)
    # Create a DP table with dimensions (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def precision(reference, candidate):
    """Calculate precision for ROUGE-L."""
    ref_tokens = tokenise(reference)
    cand_tokens = tokenise(candidate)
    lcs_len = longest_common_subsequence(ref_tokens, cand_tokens)
    return lcs_len / len(cand_tokens) if len(cand_tokens) > 0 else 0


def recall(reference, candidate):
    """Calculate recall for ROUGE-L."""
    ref_tokens = tokenise(reference)
    cand_tokens = tokenise(candidate)
    lcs_len = longest_common_subsequence(ref_tokens, cand_tokens)
    return lcs_len / len(ref_tokens) if len(ref_tokens) > 0 else 0


def rouge_l_f_score(reference, candidate):
    """Calculate ROUGE-L F-score for two text strings."""
    p = precision(reference, candidate)
    r = recall(reference, candidate)
    if p + r == 0:
        return 0.0  # Avoid division by zero
    f1 = 2 * p * r / (p + r)
    return f1


class ROUGEJudge:
    """A simple LLM-based judge that evaluates text relevance using ROUGE-L F-score."""

    def __init__(self):
        """Initialize the judge with default settings."""
        self.llm = None  # Placeholder for LLM integration if needed

    def evaluate(self, reference, candidate):
        """Evaluate the relevance of a candidate text against a reference text using ROUGE-L F-score.

        Args:
            reference (str): The reference text for comparison.
            candidate (str): The candidate text to evaluate.

        Returns:
            dict: A dictionary containing the ROUGE-L F-score.
        """
        score = rouge_l_f_score(reference, candidate)
        return {"rouge_l_f1": score}


if __name__ == "__main__":
    # Example usage (commented out; uncomment to test)
    reference_text = "The quick brown fox jumps over the lazy dog."
    candidate_text = "The quick fox leaps over the lazy dog."
    judge = ROUGEJudge()
    evaluation = judge.evaluate(reference_text, candidate_text)
    logger.info(f"Evaluation Result: {evaluation}")

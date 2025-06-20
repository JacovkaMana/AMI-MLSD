from loguru import logger
import json


def tokenise(text):
    """Tokenize text into words for ROUGE calculation."""
    return text.split()


def longest_common_subsequence(A, B):
    """Compute the length of the longest common subsequence between two lists of words."""
    m = len(A)
    n = len(B)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def rouge_l_f_score(reference, candidate):
    """Calculate ROUGE-L F-score for two text strings."""
    ref_tokens = tokenise(reference)
    cand_tokens = tokenise(candidate)
    lcs_len = longest_common_subsequence(ref_tokens, cand_tokens)

    precision = lcs_len / len(cand_tokens) if len(cand_tokens) > 0 else 0
    recall = lcs_len / len(ref_tokens) if len(ref_tokens) > 0 else 0

    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


class RougeLJudge:
    def __init__(self):
        self.metric_name = "rouge_l"

    def evaluate(self, query, result, reference_dataset=None):
        """Evaluate using ROUGE-L against query or reference dataset."""
        if reference_dataset:
            if isinstance(reference_dataset, str):
                references = [reference_dataset]
            elif isinstance(reference_dataset, (list, dict)):
                references = (
                    list(reference_dataset.values())
                    if isinstance(reference_dataset, dict)
                    else reference_dataset
                )
            else:
                references = [str(reference_dataset)]

            scores = [rouge_l_f_score(ref, result) * 100 for ref in references]
            score = max(scores)  # Use highest score
        else:
            score = rouge_l_f_score(query, result)

        return {
            "score": score,
            "explanation": f"ROUGE-L similarity score: {score:.4f}",
        }


if __name__ == "__main__":
    # Test case
    judge = RougeLJudge()
    test_eval = judge.evaluate(
        "The quick brown fox jumps over the lazy dog",
        "The quick fox leaps over the lazy dog",
    )
    logger.info(f"Test evaluation: {json.dumps(test_eval, indent=2)}")

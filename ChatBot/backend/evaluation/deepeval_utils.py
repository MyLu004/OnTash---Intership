# from deepeval.test_case import LLMTestCase
# from deepeval.metrics import AnswerRelevancyMetric
# from deepeval import evaluate

# def evaluate_response(user_input: str, model_response: str, expected_output: str = None):
#     test_case = LLMTestCase(
#         input=user_input,
#         actual_output=model_response,
#         expected_output=expected_output or user_input
#     )

#     metric = AnswerRelevancyMetric(threshold=0.7)
#     results = evaluate(test_case, [metric])

#     return results[0].score if results else 0.0


from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval import evaluate
from deepeval.models.llms.ollama_model import OllamaModel

# Use your local model — make sure it's running in Ollama
ollama_llm = OllamaModel(model="llama3")  # or "mistral", "phi3", etc.

def evaluate_response(user_input: str, model_response: str, expected_output: str = None):
    test_case = LLMTestCase(
        input=user_input,
        actual_output=model_response,
        expected_output=expected_output or user_input
    )

    metric = AnswerRelevancyMetric(threshold=0.7, model=ollama_llm)
    result = evaluate([test_case], [metric]) 
    return result.test_results[0].metrics_data[0].score if result else 0.0
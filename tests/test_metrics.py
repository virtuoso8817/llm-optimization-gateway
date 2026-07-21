from core.metrics import PromptMetrics

metrics = PromptMetrics()

sample_prompts = [

"""
Could you kindly explain Vector Databases?
""",

"""
Please Please Please explain
Transformers!!!!!!!!!!!
""",

"""
Hello




World
""",

"""
Can you kindly tell me about Retrieval Augmented Generation?
"""

]

for i, prompt in enumerate(sample_prompts, start=1):

    print("=" * 70)
    print(f"TEST {i}")

    result = metrics.analyze(prompt)

    for key, value in result.items():
        print(f"{key}:")
        print(value)
        print()
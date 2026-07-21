from core.metrics import PromptMetrics
from database.db import DatabaseManager

metrics_engine = PromptMetrics()
database = DatabaseManager()

sample_prompt = """
Could you kindly please please explain explain
Vector Databases!!!!!!!!!!
"""

metrics = metrics_engine.analyze(sample_prompt)

database.insert_metrics(metrics)

print("Inserted Successfully!\n")

print("All Records:\n")

for row in database.get_all_metrics():
    print(row)

print("\nSummary:\n")

print(database.get_summary())
from database.db import DatabaseManager

db = DatabaseManager()

logs = db.get_all_llm_logs()

print("Total Logs:", len(logs))

for log in logs:
    print(log)


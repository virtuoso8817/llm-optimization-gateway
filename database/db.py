"""
db.py

SQLite database manager for storing prompt optimization metrics
and LLM request logs.
"""

import sqlite3
from datetime import datetime


class DatabaseManager:

    def __init__(self, db_name="database/database.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Create all required tables."""

        conn = self.connect()
        cursor = conn.cursor()

        # ==========================================
        # Prompt Optimization Metrics
        # ==========================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompt_metrics (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,

            original_prompt TEXT,
            optimized_prompt TEXT,

            optimization_applied INTEGER,

            original_chars INTEGER,
            optimized_chars INTEGER,
            chars_saved INTEGER,
            character_compression REAL,

            original_tokens INTEGER,
            optimized_tokens INTEGER,
            tokens_saved INTEGER,
            compression_ratio REAL

        )
        """)

        # ==========================================
        # LLM Request Logs
        # ==========================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS llm_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,

            provider TEXT,
            model TEXT,

            prompt TEXT,
            response TEXT,

            latency_ms REAL,

            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER,

            input_cost REAL,
            output_cost REAL,
            total_cost REAL

        )
        """)

        conn.commit()
        conn.close()

    # ==========================================================
    # INSERT METHODS
    # ==========================================================

    def insert_metrics(self, metrics: dict):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO prompt_metrics(

            timestamp,

            original_prompt,
            optimized_prompt,

            optimization_applied,

            original_chars,
            optimized_chars,
            chars_saved,
            character_compression,

            original_tokens,
            optimized_tokens,
            tokens_saved,
            compression_ratio

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            metrics["original_prompt"],
            metrics["optimized_prompt"],

            int(metrics["optimization_applied"]),

            metrics["original_chars"],
            metrics["optimized_chars"],
            metrics["chars_saved"],
            metrics["character_compression"],

            metrics["original_tokens"],
            metrics["optimized_tokens"],
            metrics["tokens_saved"],
            metrics["compression_ratio"]

        ))

        conn.commit()
        conn.close()

    def insert_llm_log(self, log: dict):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO llm_logs(

            timestamp,
            provider,
            model,

            prompt,
            response,

            latency_ms,

            prompt_tokens,
            completion_tokens,
            total_tokens,

            input_cost,
            output_cost,
            total_cost

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            log["provider"],
            log["model"],

            log["prompt"],
            log["response"],

            log["latency_ms"],

            log["prompt_tokens"],
            log["completion_tokens"],
            log["total_tokens"],

            log["input_cost"],
            log["output_cost"],
            log["total_cost"]

        ))

        conn.commit()
        conn.close()

    # ==========================================================
    # HISTORY
    # ==========================================================

    def get_all_metrics(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM prompt_metrics ORDER BY id DESC")

        rows = cursor.fetchall()

        conn.close()

        return rows

    def get_all_llm_logs(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM llm_logs ORDER BY id DESC")

        rows = cursor.fetchall()

        conn.close()

        return rows

    # ==========================================================
    # ANALYTICS
    # ==========================================================

    def get_summary(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            COUNT(*),
            SUM(chars_saved),
            SUM(tokens_saved),
            AVG(character_compression),
            AVG(compression_ratio)

        FROM prompt_metrics

        """)

        result = cursor.fetchone()

        conn.close()

        return {

            "total_prompts": result[0] or 0,
            "total_characters_saved": result[1] or 0,
            "total_tokens_saved": result[2] or 0,
            "average_character_compression": round(result[3] or 0, 2),
            "average_token_compression": round(result[4] or 0, 2)

        }

    def get_cost_summary(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            COUNT(*),
            SUM(total_cost),
            AVG(total_cost),

            SUM(prompt_tokens),
            SUM(completion_tokens),
            SUM(total_tokens)

        FROM llm_logs

        """)

        result = cursor.fetchone()

        conn.close()

        return {

            "total_requests": result[0] or 0,
            "total_cost": round(result[1] or 0, 6),
            "average_cost": round(result[2] or 0, 6),

            "prompt_tokens": result[3] or 0,
            "completion_tokens": result[4] or 0,
            "total_tokens": result[5] or 0

        }

    def get_model_statistics(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            model,
            COUNT(*),
            AVG(latency_ms),
            AVG(total_cost),
            AVG(prompt_tokens),
            AVG(completion_tokens)

        FROM llm_logs

        GROUP BY model

        """)

        rows = cursor.fetchall()

        conn.close()

        return [

            {

                "model": row[0],
                "requests": row[1],
                "average_latency_ms": round(row[2] or 0, 2),
                "average_cost": round(row[3] or 0, 6),
                "average_prompt_tokens": round(row[4] or 0, 2),
                "average_completion_tokens": round(row[5] or 0, 2)

            }

            for row in rows

        ]

    def get_daily_trends(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            DATE(timestamp),
            COUNT(*),
            SUM(tokens_saved),
            SUM(chars_saved)

        FROM prompt_metrics

        GROUP BY DATE(timestamp)

        ORDER BY DATE(timestamp)

        """)

        rows = cursor.fetchall()

        conn.close()

        return [

            {

                "date": row[0],
                "prompts": row[1],
                "tokens_saved": row[2] or 0,
                "characters_saved": row[3] or 0

            }

            for row in rows

        ]

    def get_optimization_statistics(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            COUNT(*),

            SUM(
                CASE
                    WHEN optimization_applied = 1
                    THEN 1
                    ELSE 0
                END
            ),

            AVG(tokens_saved),
            MAX(tokens_saved),

            AVG(compression_ratio),
            MAX(compression_ratio)

        FROM prompt_metrics

        """)

        result = cursor.fetchone()

        conn.close()

        total = result[0] or 0
        optimized = result[1] or 0

        return {

            "optimization_rate":
                round((optimized / total) * 100, 2) if total else 0,

            "average_tokens_saved":
                round(result[2] or 0, 2),

            "maximum_tokens_saved":
                result[3] or 0,

            "average_compression":
                round(result[4] or 0, 2),

            "maximum_compression":
                round(result[5] or 0, 2)

        }


if __name__ == "__main__":

    db = DatabaseManager()

    print("Database initialized successfully!")
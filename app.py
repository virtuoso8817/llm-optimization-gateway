from fastapi import FastAPI
from pydantic import BaseModel

from core.prompt_optimizer import PromptOptimizer
from core.metrics import PromptMetrics
from database.db import DatabaseManager
from services.llm_service import LLMService

# =====================================================
# Initialize Components
# =====================================================

prompt_optimizer = PromptOptimizer()
metrics_engine = PromptMetrics()
database = DatabaseManager()
llm_service = LLMService()

# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(
    title="LLM Optimization Gateway",
    description="Middleware for prompt optimization and token analytics",
    version="1.0.0"
)

# =====================================================
# Request Models
# =====================================================

class PromptRequest(BaseModel):
    prompt: str


class ChatRequest(BaseModel):
    prompt: str
    provider: str | None = None


# =====================================================
# Root Endpoint
# =====================================================

@app.get("/")
def root():
    return {
        "message": "LLM Optimization Gateway is running!"
    }


# =====================================================
# Prompt Optimization
# =====================================================

@app.post("/optimize",summary="Optimize a prompt without calling an LLM")
def optimize_prompt(request: PromptRequest):
     
    optimization = prompt_optimizer.optimize(request.prompt)

    report = metrics_engine.generate(
        original_prompt=optimization.original_prompt,
        optimized_prompt=optimization.optimized_prompt,
        token_stats={
            "original_tokens": optimization.original_tokens,
            "optimized_tokens": optimization.optimized_tokens,
            "tokens_saved": optimization.tokens_saved,
            "compression_ratio": optimization.token_compression_percent,
        },
    )

    report["optimization_applied"] = optimization.optimization_applied

    report["original_chars"] = optimization.original_chars
    report["optimized_chars"] = optimization.optimized_chars
    report["chars_saved"] = optimization.chars_saved
    report["character_compression"] = optimization.compression_percent

    database.insert_metrics(report)

    return report


# =====================================================
# Chat Endpoint
# =====================================================

@app.post("/chat",summary="Generate an AI response using an automatically optimized prompt")
def chat(request: ChatRequest):

    # -----------------------------------------
    # Step 1: Optimize Prompt
    # -----------------------------------------

    optimization = prompt_optimizer.optimize(request.prompt)

    # -----------------------------------------
    # Step 2: Send Optimized Prompt to LLM
    # -----------------------------------------

    llm_response = llm_service.chat(
        prompt=optimization.optimized_prompt,
        provider=request.provider
    )

    # -----------------------------------------
    # Step 3: Estimate Original Prompt Cost
    # -----------------------------------------

    prompt_tokens = llm_response["prompt_tokens"]

    optimized_tokens = optimization.optimized_tokens
    original_tokens = optimization.original_tokens

    if optimized_tokens > 0:

        estimated_original_prompt_tokens = int(
            prompt_tokens * original_tokens / optimized_tokens
        )

    else:

        estimated_original_prompt_tokens = prompt_tokens

    input_cost = llm_response["input_cost"]

    estimated_original_input_cost = (
        input_cost * estimated_original_prompt_tokens / prompt_tokens
        if prompt_tokens > 0 else input_cost
    )

    cost_saved = estimated_original_input_cost - input_cost

    # -----------------------------------------
    # Step 4: Merge Response
    # -----------------------------------------

    llm_response["original_prompt"] = optimization.original_prompt
    llm_response["optimized_prompt"] = optimization.optimized_prompt

    llm_response["original_tokens"] = optimization.original_tokens
    llm_response["optimized_tokens"] = optimization.optimized_tokens
    llm_response["tokens_saved"] = optimization.tokens_saved

    llm_response["estimated_original_input_cost"] = round(
        estimated_original_input_cost,
        8
    )

    llm_response["actual_input_cost"] = round(
        input_cost,
        8
    )

    llm_response["estimated_cost_saved"] = round(
        cost_saved,
        8
    )

    return llm_response

# =====================================================
# Analytics Endpoints
# =====================================================

@app.get("/analytics/summary",summary="View overall prompt optimization statistics")
def analytics_summary():
    return database.get_summary()


@app.get("/analytics/cost",summary="View cumulative LLM usage cost")
def analytics_cost():
    return database.get_cost_summary()


@app.get("/analytics/models",summary="View model-wise usage statistics")
def analytics_models():
    return database.get_model_statistics()


@app.get("/analytics/trends",summary="View prompt optimization history")
def analytics_trends():
    return database.get_daily_trends()


@app.get("/analytics/statistics",)
def analytics_statistics():
    return database.get_optimization_statistics()


# =====================================================
# History Endpoints
# =====================================================

@app.get("/history",summary="View prompt optimization history")
def get_history():

    records = database.get_all_metrics()

    history = []

    for row in records:

        history.append({

            "id": row[0],
            "timestamp": row[1],

            "original_prompt": row[2],
            "optimized_prompt": row[3],

            "optimization_applied": bool(row[4]),

            "original_chars": row[5],
            "optimized_chars": row[6],
            "chars_saved": row[7],
            "character_compression": row[8],

            "original_tokens": row[9],
            "optimized_tokens": row[10],
            "tokens_saved": row[11],
            "compression_ratio": row[12]

        })

    return history


@app.get("/llm-history",summary="View LLM request history")
def llm_history():
    return database.get_all_llm_logs()
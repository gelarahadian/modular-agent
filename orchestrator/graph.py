from typing import TypedDict, Optional


class AgentState(TypedDict):
    task: str
    intake_category: Optional[str]
    intake_reasoning: Optional[str]
    execution_result: Optional[str]
    execution_reasoning: Optional[str]
    execution_confidence: Optional[float]
    validation_approved: Optional[bool]
    validation_feedback: Optional[str]
    retry_count: Optional[int]


from langgraph.graph import StateGraph, END

from agents.intake_agent import intake_agent
from agents.execution_agent import execution_agent
from agents.validation_agent import validation_agent

def intake_node(state: AgentState):
    result = intake_agent(state["task"])
    return {
        "intake_category": result.category,
        "intake_reasoning": result.reasoning,
    }


def execution_node(state: AgentState):
    feedback = state.get('validation_feedback', '')

    enriched_task = state['task']

    if feedback:
        enriched_task += f"\n\nPrevios validation feedback: {feedback}"

    result = execution_agent(enriched_task)

    current_retry = state.get('retry_count', 0)

    return {
        "execution_result": result.result,
        "execution_reasoning": result.reasoning,
        "execution_confidence": result.confidence,
        'retry_count': current_retry + 1,
    }


def validation_node(state: AgentState):
    result = validation_agent(
        state["task"],
        state["execution_result"],
    )
    return {
        "validation_approved": result.approved,
        "validation_feedback": result.feedback,
    }

def route_after_validation(state: AgentState):
    if state["validation_approved"]:
        return END
    
    if state["retry_count"] >= 2:
        return END
    
    return "execution"

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("intake", intake_node)
    workflow.add_node("execution", execution_node)
    workflow.add_node("validation", validation_node)

    workflow.set_entry_point("intake")

    workflow.add_edge("intake", "execution")
    workflow.add_edge("execution", "validation")

    workflow.add_conditional_edges(
        "validation",
        route_after_validation,
        {
            END: END,
            "execution": "execution",
        },
    )

    return workflow.compile()

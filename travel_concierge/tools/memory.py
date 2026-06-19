"""Tools for storing and retrieving trip information from session state."""

from google.adk.tools import ToolContext


def memorize(key: str, value: str, tool_context: ToolContext) -> dict:
    """Store a piece of trip information (one key-value pair at a time).

    Args:
        key: Label for the information (e.g. 'destination', 'travel_dates').
        value: The information to store.
        tool_context: ADK tool context (provides session state).

    Returns:
        A status message confirming what was stored.
    """
    tool_context.state[key] = value
    return {"status": f'Stored "{key}": "{value}"'}


def recall(key: str, tool_context: ToolContext) -> dict:
    """Retrieve a previously stored piece of trip information.

    Args:
        key: The label of the information to retrieve.
        tool_context: ADK tool context (provides session state).

    Returns:
        The stored value, or a message indicating it was not found.
    """
    value = tool_context.state.get(key)
    if value is None:
        return {"status": "not_found", "key": key}
    return {"status": "found", "key": key, "value": value}

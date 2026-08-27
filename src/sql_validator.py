def validate_sql(query: str) -> tuple[bool, str]:

    query = query.strip()

    if not query:
        return False, "SQL query cannot be empty."

    if not query.lower().startswith("select"):
        return False, "Only SELECT queries are allowed."

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "copy"
    ]

    query_lower = query.lower()

    for keyword in forbidden_keywords:

        if keyword in query_lower:
            return False, (
                f"SQL operation '{keyword.upper()}' "
                "is not allowed."
            )

    return True, "SQL query is valid."
def xpath_to_lower(term: str) -> str:
    return f"translate({term}, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"


def xpath_string_upper() -> str:
    return f"translate(string(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')"


def xpath_string_lower() -> str:
    return xpath_to_lower("string()")


def xpath_contains(container: str, contained: str) -> str:
    return f"contains({container}, \"{contained}\")"


def xpath_exact_match(term: str, keyword: str) -> str:
    return f"{term} = \"{keyword}\""


def xpath_not(term: str) -> str:
    return f"not({term})"

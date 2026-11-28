import re


def pattern(regex):
    compiled = re.compile(regex)

    def matches(value):
        return compiled.fullmatch(value) is not None

    matches.__name__ = f'pattern({regex})'
    return matches

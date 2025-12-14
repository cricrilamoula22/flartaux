import re

VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")

class FusionTemplateError(Exception):
    pass


def render_conditional_text(template: str, context: dict) -> str:
    lines = template.splitlines()
    output = []
    stack = []

    for raw_line in lines:
        line = raw_line.rstrip()

        if line.startswith("IF ") and line.endswith(":"):
            condition = line[3:-1].strip()
            stack.append(bool(context.get(condition)))
            continue

        if line == "ELSE:":
            if not stack:
                raise FusionTemplateError("ELSE sans IF")
            stack[-1] = not stack[-1]
            continue

        if line == "ENDIF":
            if not stack:
                raise FusionTemplateError("ENDIF sans IF")
            stack.pop()
            continue

        if all(stack):
            def replace_var(match):
                key = match.group(1)
                return str(context.get(key, ""))

            output.append(VAR_PATTERN.sub(replace_var, line))

    if stack:
        raise FusionTemplateError("IF non fermé")

    return "\n".join(output)

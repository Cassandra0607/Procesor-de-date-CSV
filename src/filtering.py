import re

OPS = ["<=", ">=", "=", ">", "<"]

def _parse_one_condition(cond: str):
    cond = cond.strip()

    op = None
    for candidate in OPS:
        if candidate in cond:
            op = candidate
            break
    if op is None:
        raise ValueError(f"Conditie invalida: {cond}")

    left, right = cond.split(op, 1)
    col = left.strip()
    raw = right.strip()

    if (raw.startswith("'") and raw.endswith("'")) or (raw.startswith('"') and raw.endswith('"')):
        value = raw[1:-1]
        value_type = "str"
    else:
        try:
            value = float(raw)
            value_type = "num"
        except ValueError:
            value = raw
            value_type = "str"

    return col, op, value, value_type

def _eval_condition(row, col, op, value, value_type):
    if col not in row:
        return False

    cell_raw = row[col]

    if value_type == "num":
        try:
            cell = float(cell_raw)
        except ValueError:
            return False
        rhs = value
    else:
        cell = str(cell_raw)
        rhs = str(value)

    if op == "=":
        return cell == rhs
    if op == ">":
        return cell > rhs
    if op == "<":
        return cell < rhs
    if op == ">=":
        return cell >= rhs
    if op == "<=":
        return cell <= rhs
    return False

def filter_rows_expression(rows, expr: str):

    or_parts = [p.strip() for p in re.split(r"\s+OR\s+", expr.strip()) if p.strip()]

    parsed_or = []
    for part in or_parts:
        and_parts = [a.strip() for a in re.split(r"\s+AND\s+", part) if a.strip()]
        parsed_and = [_parse_one_condition(c) for c in and_parts]
        parsed_or.append(parsed_and)

    filtered = []
    for row in rows:
        ok_or = False
        for and_clause in parsed_or:
            ok_and = True
            for (col, op, value, vtype) in and_clause:
                if not _eval_condition(row, col, op, value, vtype):
                    ok_and = False
                    break
            if ok_and:
                ok_or = True
                break
        if ok_or:
            filtered.append(row)

    return filtered

def filter_rows(rows, column, operator, value):
    filtered = []
    for row in rows:
        try:
            cell = float(row[column])
            value_float = float(value)
        except ValueError:
            cell = row[column]
            value_float = value

        if operator == "=":
            if cell == value_float:
                filtered.append(row)
        elif operator == ">":
            if cell > value_float:
                filtered.append(row)
        elif operator == "<":
            if cell < value_float:
                filtered.append(row)
        elif operator == ">=":
            if cell >= value_float:
                filtered.append(row)
        elif operator == "<=":
            if cell <= value_float:
                filtered.append(row)

    return filtered

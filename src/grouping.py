from stats import mean

def group_by(rows, group_column, agg_instructions):
    groups = {}
    for row in rows:
        key = row[group_column]
        if key not in groups:
            groups[key] = []
        groups[key].append(row)

    result = {}
    for key, group_rows in groups.items():
        result[key] = {}
        for instr in agg_instructions:
            op, col = instr.split(":")
            values = []
            for r in group_rows:
                try:
                    values.append(float(r[col]))
                except ValueError:
                    continue
            if op == "sum":
                result[key][instr] = sum(values)
            elif op == "avg":
                result[key][instr] = mean(values)
            elif op == "count":
                result[key][instr] = len(values)
    return result

def sort_rows(rows, columns):
    for col in reversed(columns):
        try:
            rows.sort(key=lambda x: float(x[col]))
        except ValueError:
            # daca nu merge, sortam ca string
            rows.sort(key=lambda x: x[col])
    return rows

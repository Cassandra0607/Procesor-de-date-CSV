from collections import Counter
from stats import mean, median, mode

MISSING = {"", "na", "n/a", "null", "none"}

def is_missing(v):
    if v is None:
        return True
    s = str(v).strip().lower()
    return s in MISSING

def try_float(v):
    if is_missing(v):
        return None
    s = str(v).strip()
    if "," in s and "." not in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

def get_numeric_column(rows, col):
    vals = []
    for r in rows:
        x = try_float(r.get(col, ""))
        if x is not None:
            vals.append(x)
    return vals

def fill_missing(rows, headers, method: str):
    method = method.strip().lower()

    # value:XYZ
    literal = None
    if method.startswith("value:"):
        literal = method.split(":", 1)[1]

    fill_map = {}
    if method in {"mean", "median", "mode"}:
        for h in headers:
            nums = get_numeric_column(rows, h)
            if nums:
                if method == "mean":
                    fill_map[h] = mean(nums)
                elif method == "median":
                    fill_map[h] = median(nums)
                else:
                    fill_map[h] = mode(nums)

    for r in rows:
        for h in headers:
            if is_missing(r.get(h, "")):
                if method == "zero":
                    r[h] = "0"
                elif literal is not None:
                    r[h] = literal
                elif h in fill_map:
                    r[h] = str(fill_map[h])
                else:
                    r[h] = r.get(h, "")
    return rows

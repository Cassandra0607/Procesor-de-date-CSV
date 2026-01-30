import math
from cleaning import try_float, is_missing

def pearson(rows, col1, col2):
    xs, ys = [], []
    for r in rows:
        a = r.get(col1, "")
        b = r.get(col2, "")
        if is_missing(a) or is_missing(b):
            continue
        x = try_float(a)
        y = try_float(b)
        if x is None or y is None:
            continue
        xs.append(x)
        ys.append(y)

    n = len(xs)
    if n < 2:
        return None, n

    mx = sum(xs) / n
    my = sum(ys) / n

    num = sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
    denx = math.sqrt(sum((x-mx)**2 for x in xs))
    deny = math.sqrt(sum((y-my)**2 for y in ys))

    if denx == 0 or deny == 0:
        return None, n
    return num / (denx * deny), n

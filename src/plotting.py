from cleaning import try_float

def histogram(rows, col, bins=10, width=40):
    vals = []
    for r in rows:
        x = try_float(r.get(col, ""))
        if x is not None:
            vals.append(x)

    if not vals:
        print(f"Nu exista valori numerice pentru coloana '{col}'.")
        return

    mn, mx = min(vals), max(vals)
    if mn == mx:
        print(f"Toate valorile din '{col}' sunt {mn}.")
        return

    bin_size = (mx - mn) / bins
    counts = [0] * bins
    for v in vals:
        idx = int((v - mn) / bin_size)
        if idx == bins:
            idx -= 1
        counts[idx] += 1

    maxc = max(counts)
    print(f"Histograma pentru '{col}' (n={len(vals)}, bins={bins})")
    for i, c in enumerate(counts):
        lo = mn + i * bin_size
        hi = lo + bin_size
        bar_len = int((c / maxc) * width) if maxc else 0
        bar = "#" * bar_len
        print(f"{lo:>10.2f} - {hi:>10.2f} | {bar} ({c})")

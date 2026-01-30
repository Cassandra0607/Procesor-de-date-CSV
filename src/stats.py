def mean(values):
    return sum(values) / len(values) if len(values) > 0 else 0

def median(values):
    n = len(values)
    if n == 0:
        return 0

    sorted_values = sorted(values)  # sortăm lista
    mid = n // 2

    if n % 2 == 0:
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2
    else:
        return sorted_values[mid]

def mode(values):
    if not values:
        return 0

    frequency = {}
    for v in values:
        if v in frequency:
            frequency[v] += 1
        else:
            frequency[v] = 1

    max_count = max(frequency.values())
    for key, count in frequency.items():
        if count == max_count:
            return key

def minimum(values):
    return min(values) if values else 0

def maximum(values):
    return max(values) if values else 0

def stddev(values):
    n = len(values)
    if n == 0:
        return 0

    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / n
    return variance ** 0.5

def percentile(values, percent):
    n = len(values)
    if n == 0:
        return 0

    sorted_values = sorted(values)
    k = (n - 1) * (percent / 100)
    f = int(k)
    c = f + 1

    if c >= n:
        return sorted_values[f]

    d0 = sorted_values[f] * (c - k)
    d1 = sorted_values[c] * (k - f)
    return d0 + d1

import csv

CANDIDATES = [",", ";", "\t", "|"]

def read_csv(file_path):
    with open(file_path, newline="", encoding="utf-8") as file:
        sample = file.read(4096)
        file.seek(0)

        delimiter = None
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters="".join(CANDIDATES))
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = None

        first_line = file.readline()
        file.seek(0)

        if delimiter is None:
            delimiter = max(CANDIDATES, key=lambda d: len(first_line.split(d)))

        reader = csv.DictReader(file, delimiter=delimiter)

        headers = reader.fieldnames or []
        headers = [h.strip() for h in headers]

        rows = []
        for row in reader:
            fixed = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
            rows.append(fixed)

    return headers, rows

from stats import mean, median, mode, minimum, maximum, stddev, percentile
import argparse
from reader import read_csv
from sorting import sort_rows
from grouping import group_by


def main():
    parser = argparse.ArgumentParser(description="Procesor CSV")

    parser.add_argument("input_file", help="Fisier CSV de intrare")

    parser.add_argument("--stats", help="Calculeaza statistici pentru o coloana (numeric)")
    parser.add_argument("--filter", help="Filtrare randuri: Pret>100 AND Categorie='Electronice'")
    parser.add_argument("--sort", help="Sortare dupa coloane separate prin virgula, ex: Pret,Vanzari")
    parser.add_argument("--groupby", help="Grupare dupa o coloana")
    parser.add_argument("--agg", help="Agregari separate prin virgula, ex: sum:Vanzari,avg:Pret,count:Pret")

    parser.add_argument("--correlation", nargs=2, metavar=("COL1", "COL2"),
                        help="Corelatie Pearson intre 2 coloane numerice")
    parser.add_argument("--plot", nargs=2, metavar=("TYPE", "COL"),
                        help="Plot in terminal. Ex: --plot histogram Varsta")
    parser.add_argument("--clean", nargs=1, help="Curatare: missing")
    parser.add_argument("--fill", nargs=1, help="Umplere lipsuri: mean/median/mode/zero/value:XXX")
    parser.add_argument("--output", help="Exporta datele finale intr-un CSV nou")

    args = parser.parse_args()

    headers, rows = read_csv(args.input_file)

    print("Coloane detectate:", headers)
    print("Numar randuri:", len(rows))
    print("Fisier primit:", args.input_file)

    if args.clean and args.clean[0].lower() == "missing":
        if not args.fill:
            print("Ai cerut --clean missing dar lipseste --fill (mean/median/mode/zero/value:XXX)")
        else:
            from cleaning import fill_missing
            rows = fill_missing(rows, headers, args.fill[0])
            print("Missing values completate cu:", args.fill[0])

    if args.filter:
        from filtering import filter_rows_expression
        try:
            rows = filter_rows_expression(rows, args.filter)
            print(f"Numar randuri dupa filtrare: {len(rows)}")
        except Exception as e:
            print("Eroare la filtrare:", e)

    if args.sort:
        columns_to_sort = [col.strip() for col in args.sort.split(",") if col.strip()]
        rows = sort_rows(rows, columns_to_sort)
        print("Randuri sortate dupa:", columns_to_sort)

    if args.stats:
        from cleaning import try_float

        col_values = []
        for row in rows:
            x = try_float(row.get(args.stats, ""))
            if x is not None:
                col_values.append(x)

        print("Statistici cerute pentru coloana:", args.stats)
        print("Count:", len(col_values))
        print("Mean:", mean(col_values))
        print("Median:", median(col_values))
        print("Mode:", mode(col_values))
        print("Min:", minimum(col_values))
        print("Max:", maximum(col_values))
        print("Stddev:", stddev(col_values))
        print("Percentila 25:", percentile(col_values, 25))
        print("Percentila 75:", percentile(col_values, 75))

    if args.groupby and args.agg:
        agg_list = [a.strip() for a in args.agg.split(",") if a.strip()]
        grouped_result = group_by(rows, args.groupby, agg_list)

        print(f"Agregare dupa {args.groupby}:")
        for key, agg_values in grouped_result.items():
            line = f" {key}: "
            parts = []
            for k, v in agg_values.items():
                op, col = k.split(":", 1)
                label = "mediu" if op == "avg" else ("total" if op == "sum" else "count")
                parts.append(f"{col} {label}={v}")
            line += ", ".join(parts)
            print(line)

    if args.correlation:
        from correlation import pearson

        c1, c2 = args.correlation
        r, n = pearson(rows, c1, c2)

        if r is None:
            print(f"Nu pot calcula corelatia Pearson pentru '{c1}' si '{c2}' (n={n}).")
        else:
            print(f"Corelatie Pearson({c1}, {c2}) = {r:.6f} (n={n})")

    if args.plot:
        plot_type, col = args.plot
        plot_type = plot_type.lower()

        if plot_type == "histogram":
            from plotting import histogram
            histogram(rows, col)
        else:
            print("Tip plot necunoscut. Foloseste: --plot histogram Coloana")

    if args.output:
        from exporter import export_csv
        export_csv(args.output, headers, rows)
        print("Export realizat in:", args.output)

    if not any([
        args.stats,
        args.filter,
        args.sort,
        (args.groupby and args.agg),
        args.correlation,
        args.plot,
        args.clean,
        args.output
    ]):
        print("Nu s-a cerut nicio operatie.")


if __name__ == "__main__":
    main()

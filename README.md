# Procesor de date CSV

Acest proiect este un procesor de fisiere CSV scris in Python. Aplicatia permite prelucrarea si analiza datelor dintr-un CSV direct din terminal, fara sa folosesc librarii externe precum pandas.

## Autor
- Nume: Toader Cassandra Iulia
- Grupa: 3.2
- Email: cassandra-iulia.toader@student.upt.ro
- An academic: 2025-2026

## Descriere
Aplicatia citeste un fisier CSV si permite mai multe operatii pe date tabulare. Programul poate calcula statistici pe coloane numerice, poate filtra randuri dupa conditii, poate sorta datele, poate grupa datele si aplica agregari, poate completa valori lipsa si poate exporta rezultatele intr-un fisier nou.

Scopul proiectului este sa ofer o varianta simpla pentru procesarea CSV-urilor, asemanatoare cu unele functii din Excel sau pandas, dar implementata manual.

## Tehnologii folosite
- Limbaj: Python 3.x
- Biblioteci:
  - csv - citire si scriere fisiere CSV
  - argparse - argumente din linia de comanda
  - re - filtrare cu expresii de tip AND/OR
  - math - calcule matematice (corelatie Pearson)
  - collections - operatii cu frecvente
- Tools: Git, GitHub, GitHub Actions, Docker (optional)

## Cerinte sistem
- Python 3.x (recomandat 3.10+)
- Sistem de operare: Windows / Linux / macOS
- Nu sunt necesare dependente externe

## Instalare
```bash
git clone https://github.com/username/project.git
cd project

Comenzi rulare:
python src/main.py data/test.csv

Comenzi disponibile si exemple:
python src/main.py data/test.csv --stats Pret
python src/main.py data/test.csv --filter "Pret>100 AND Categorie='Electronice'"
python src/main.py data/test.csv --filter "Categorie='Alimente' OR Pret<20"
python src/main.py data/test.csv --sort Pret,Vanzari
python src/main.py data/test.csv --groupby Categorie --agg "avg:Pret,sum:Vanzari,count:Pret"
python src/main.py data/test.csv --correlation Pret Vanzari
python src/main.py data/test.csv --plot histogram Varsta
python src/main.py data/test.csv --clean missing --fill mean --output data/clean.csv
python src/main.py data/test.csv --filter "Pret>100" --output data/filtered.csv
python src/main.py data/test.csv --clean missing --fill mean --filter "Pret>100 AND Categorie='Electronice'" --sort Pret --output data/final.csv

Functionalitati implementate:
[x] Citire CSV cu detectarea automata a delimitatorului
[x] Statistici pe coloane: mean, median, mode, min, max, stddev, percentile
[x] Filtrare randuri dupa conditii (suporta AND si OR)
[x] Sortare dupa una sau mai multe coloane
[x] Calcul corelatii intre coloane numerice (Pearson)
[x] Grupare dupa coloane si agregari (sum, avg, count)
[x] Detectare valori lipsa si completare (clean missing + fill)
[x] Export date filtrate/procesate in CSV
[x] Histograme text pentru date numerice

Structura:
project/
├── README.md
├── Dockerfile
├── .github/
│   └── workflows/
│       └── build.yaml
├── src/
│   ├── main.py
│   ├── reader.py
│   ├── stats.py
│   ├── filtering.py
│   ├── sorting.py
│   ├── grouping.py
│   ├── cleaning.py
│   ├── correlation.py
│   ├── plotting.py
│   └── exporter.py
├── data/
│   └── test.csv
    └── (aici se genereaza fisierele de output)

Decizie de design:
Am folosit csv.DictReader ca sa citesc randurile sub forma de dictionare. Asa pot accesa valorile direct dupa numele coloanei si este mai usor pentru filtrare si agregari.
Am impartit proiectul pe module ca sa fie mai clar ce face fiecare parte (citire, filtrare, sortare, statistici etc).
Pentru filtrarea complexa am implementat suport AND si OR, ca sa pot combina mai multe conditii in aceeasi comanda.

Probleme intalnite si solutii:
Problema: Detectarea delimitatorului nu functiona corect la unele fisiere CSV si toate coloanele erau citite ca una singura.
Solutie: Am modificat reader.py ca sa aiba fallback si sa aleaga un delimitator corect daca Sniffer nu functioneaza bine.
Problema: Coloanele numerice aveau valori lipsa (NA, gol) si programul dadea erori la calcule.
Solutie: Am folosit functia try_float() ca sa ignor valorile invalide si am adaugat optiunea --clean missing cu --fill.
Problema: Cand rulez din src, fisierul CSV nu era gasit daca nu scriam calea corecta.
Solutie: Am pus fisierul de test in folderul data si rulez cu data/test.csv.

Testare:
Programul a fost testat manual folosind un fisier data/test.csv si comenzile de mai jos:
python src/main.py data/test.csv
python src/main.py data/test.csv --stats Pret
python src/main.py data/test.csv --filter "Pret>100 AND Categorie='Electronice'"
python src/main.py data/test.csv --filter "Categorie='Alimente' OR Pret<20"
python src/main.py data/test.csv --sort Pret
python src/main.py data/test.csv --groupby Categorie --agg "avg:Pret,sum:Vanzari,count:Pret"
python src/main.py data/test.csv --correlation Pret Vanzari
python src/main.py data/test.csv --plot histogram Varsta
python src/main.py data/test.csv --clean missing --fill mean --output data/clean.csv

Comenzi Docker:
docker build -t csv-processor .
docker run --rm csv-processor
docker run --rm csv-processor python src/main.py data/test.csv --stats Pret

# IE 421 - Data Science for Engineers Term Project (Please keep this main title in Readme as it is)

## When Oil Markets Shake, Do Burgers Tell a Different Story? A Big Mac Index Analysis
This project investigates the relationship between global oil price movements and purchasing power differences measured through The Economist's Big Mac Index. Using historical data covering 2000–2026, we examine whether changes in Brent crude oil prices are associated with changes in Big Mac currency valuation gaps across economies.
The analysis combines three data sources: The Economist's Big Mac Index, Brent crude oil prices from the U.S. Energy Information Administration (EIA), and oil production and consumption statistics from the Energy Institute. These datasets have different temporal resolutions and are integrated into one country-edition analytical panel.
Our research focuses on three questions. First, does the relationship between oil price changes and Big Mac valuation gaps differ during calm and high-movement oil market periods? Second, has this relationship remained stable across historical periods? Third, do economies classified as oil exporters and importers exhibit different valuation patterns?
We use exploratory data analysis, descriptive statistics, correlation analysis, and comparative visualizations to investigate these questions. The findings are interpreted as statistical associations rather than causal effects, with particular attention to historical data coverage, measurement limitations, and assumptions underlying oil-export classifications.
## Student Names
Members: Emir Karaçayır (123203010) · Emirhan Ahmet Yılmaz (122203035) · Berke Naim Özer (123203098) · Ahmet Halit Yalangün (123203034)

## Files (Explain each of them with a sentence)
- `data/`: Contains the cleaned Big Mac Index, Brent crude oil prices, Energy Institute oil production and consumption data, and the merged analytical dataset. Full dataset descriptions, sources, and cleaning decisions are documented in data/README.md. Raw downloads are stored in data/raw/ and are not committed.
- `scripts/`: Contains the scripts for downloading, cleaning, analyzing, and visualizing the data. download_data.py downloads the original Big Mac and EIA Brent data; preprocess.py cleans, validates, and merges the datasets, including Energy Institute PDF extraction; eda.ipynb performs exploratory analysis; and figures.py generates the project visualizations.
- `visuals/`: Includes the generated figures. (Explain which figure shows what.)
- `index.html` and `css/`: Main webpage for GitHub Pages hosting.
- `PROPOSAL.md`, `AI_USAGE.md`: Contain the project proposal and documentation of AI-assisted work.
- `requirements.txt`:  Lists the Python libraries required to run the project.
- `.github/`: Contains the automated repository checks provided by the course.

## How to run (from the repository root)
List the commands that reproduce your results, in the order they must be run.
```
pip install -r requirements.txt
python scripts/download_data.py
python scripts/preprocess.py --allow-ei-snapshot
jupyter nbconvert --to notebook --execute --inplace scripts/eda.ipynb
python scripts/figures.py
```
For the PDF-based alternative, replace the preprocessing command with:
```
python scripts/preprocess.py --ei-source pdf
```
## Key findings
-Oil-price movements: The edition-level analysis shows different descriptive relationships between Brent price movements and average Big Mac valuation-gap changes during calm and high-movement oil-market intervals, although these patterns do not establish causation.

-Historical variation: The relationship changes across the four examined periods (2001–2006, 2007–2013, 2014–2019, and 2020–2026), suggesting that the observed association is not stable across the full sample.

-Exporter/importer comparison: Economies classified as oil exporters and importers exhibit different median Big Mac valuation gaps over time, although the classification relies on estimated production-consumption balances and incomplete historical coverage.

## Hosting
The project website is prepared for hosting using GitHub Pages.

Repository: https://github.com/BILGI-IE-421/ie421-2026-2027-1-termproject-data-pilgrims

Website: https://bilgi-ie-421.github.io/ie421-2026-2027-1-termproject-data-pilgrims/

# Burgers, Barrels and Headlines: Does the Big Mac Index Still Measure Purchasing Power When Oil Shocks Hit?

**Team:** data-pilgrims · **Theme:** T7 The Connected World: trade, flights, prices

**Members:** Emir Karaçayır (123203010) · Emirhan Ahmet Yılmaz (122203035) · Berke Naim Özer (123203098) · Ahmet Halit Yalangün (123203034)

## The problem

The Big Mac Index is often taught as a simple test of purchasing power parity, but it compares slow-moving menu prices with fast-moving exchange rates, so its currency gaps may reflect temporary shocks rather than lasting differences in purchasing power. Oil is a likely source of such shocks: geopolitical news can move Brent crude within days, and oil prices move the currencies of oil-exporting and oil-importing countries. Combining daily Brent prices, a geopolitical risk index, verified oil-related news events and Big Mac data from 2000 onwards, this project examines how news drives oil prices and whether the link between oil and Big Mac currency gaps changes across countries and during major oil shocks. This helps readers judge when the index can be trusted.

## The data

| Dataset | Link | What is in it |
|ai_gpr_data_daily.csv|https://www.matteoiacoviello.com/gpr.htm|An index that uses AI to convert global news into risk scores.|
|big-mac-2025-01-01.xls|https://github.com/TheEconomist/big-mac-data|Big Mac prices and index values for about 55 economies, 2000–2025.|
|bigmac.csvs|https://bigmacindex.app/data/|Big Mac prices, exchange rates, and raw and GDP-adjusted index values for 56 economies (2000–2026).|
|RBRTEd.xls|https://www.eia.gov/dnav/pet/hist/RBRTED.htm|Daily Europe Brent crude spot prices in US dollars per barrel (1987–present).|
|Statistical Review of World Energy Narrow format.csv|https://www.energyinst.org/statistical-review/resources-and-data-downloads|Annual country-level energy data for 1965–2025, covering production, consumption, electricity, fuels, and emissions.|

## Our questions

1. How strongly are spikes in oil-related geopolitical news followed by Brent price movements, and does the response differ by type of event?
2. Does the pattern between oil prices and Big Mac measures differ during major oil-market disruption periods compared with calmer periods?
3. How has the relationship between Brent oil prices, oil-related geopolitical risk, and Big Mac Index currency gaps changed across countries from 2000 to the latest matched data, and did that pattern differ during major oil shocks compared with calmer periods?

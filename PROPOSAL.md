# When Oil Markets Shake, Do Burgers Tell a Different Story? A Big Mac Index Analysis

**Team:** data-pilgrims · **Theme:** T7 The Connected World: trade, flights, prices

**Members:** Emir Karaçayır (123203010) · Emirhan Ahmet Yılmaz (122203035) · Berke Naim Özer (123203098) · Ahmet Halit Yalangün (123203034)

## The problem

The Big Mac Index is often taught as a simple test of purchasing power parity (PPP). However, it compares slow-moving menu prices with fast-moving exchange rates, so the currency gaps it reports may partly reflect temporary shocks rather than lasting differences in purchasing power. Oil prices are a likely source of such shocks, because they move the currencies of oil-exporting and oil-importing countries in different directions. This project combines daily Brent crude prices, Big Mac Index data and Energy Institute country-level oil data from 2000 onwards. It asks whether oil price shocks distort the currency valuations implied by the Big Mac Index. It looks at how strongly Big Mac currency gaps move with oil prices, whether that link differs between oil exporters and importers, and whether it gets stronger during major oil shocks. The results will help readers judge when the index can be read as a reliable PPP signal and when it is mostly picking up oil-driven currency movements.

## The data

| Dataset | Link | What is in it |
|---|---|---|
|big-mac-2025-01-01.xls|https://github.com/TheEconomist/big-mac-data|Big Mac prices and index values for about 55 economies, 2000–2025.|
|bigmac.csvs|https://bigmacindex.app/data/|Big Mac prices, exchange rates, and raw and GDP-adjusted index values for 56 economies (2000–2026).|
|RBRTEd.xls|https://www.eia.gov/dnav/pet/hist/RBRTED.htm|Daily Europe Brent crude spot prices in US dollars per barrel (1987–present).|
|Statistical Review of World Energy Narrow format.csv|https://www.energyinst.org/statistical-review/resources-and-data-downloads|Annual country-level energy data for 1965–2025, covering production, consumption, electricity, fuels, and emissions.|

## Our questions

1. Is the association between Brent price changes and Big Mac currency gaps stronger in periods of high oil-price volatility than in calm periods?
2. Is the relationship between Brent and Big Mac currency gaps stable over time, or does it strengthen and weaken across 2000–2025?
3. How much of the cross-country spread in Big Mac currency gaps is explained by the difference between oil exporters and oil importers, and does that share grow when oil prices are higher?

# Data rights and provenance

## Original code

The MIT license in `LICENSE` applies only to original code in this repository. It does not license third-party source files, data, or materials.

## AEMO-derived material

The compact Wivenhoe tables and filtered source extract are derived from AEMO public DISPATCHLOAD and event records. They are accompanied by source-vintage metadata, official URLs, file hashes, AEMO field definitions, and attribution information. AEMO’s published copyright permission allows use of AEMO Material with accurate and appropriate attribution to AEMO; the source description and AEMO attribution are retained in `data/README.md` and `data/source_manifest.csv`.

Only the filtered project extract and derived tables are included; the original monthly ZIP archives are not. The repository makes no claim that it contains every upstream record or can reconstruct the analysis from all original raw sources.

## Hatta-derived material

The Hatta CSV tables in `data/hatta_derived/` and results in `verification/r26r3/` are derived calculation outputs, not confidential DEWA telemetry. They preserve the R26R3 scientific lock and do not include the original OECD ICIO archive. The original OECD 2016–2022 ZIP was not verified as preserved in the project backup. No OECD data are redistributed here.

## Source links

- AEMO copyright permissions: https://www.aemo.com.au/privacy-and-legal-notices/copyright-permissions
- AEMO MMS data model: https://visualisations.aemo.com.au/aemo/nemweb/MMSDataModelReport/Electricity/MMS%20Data%20Model%20Report_files/MMS_128.htm
- AEMO NEMWeb archive: https://nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2025/
- OECD ICIO source route (original archive absent): https://webfs-sti.oecd.org/files/STI-PIE/ICIO/2025/2016-2022_SML.zip

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Demo sandbox for BIM data dictionary development and QA automation — Accenture AI Champion Network webinar, June 2026. The domain is **Underground Utilities (UGU)**: Pipe, Conduit, Manhole, Valve.

## Four-Stage Pipeline

```
Information Requirements → Data Dictionary → Data Sheets → IFC Model
```

1. **Information Requirements (IR):** Client-supplied Excel workbook specifying asset properties and groupings (`information_requirements/`)
2. **Data Dictionary (DD):** Structured CSV definitions — objects, templates, properties, property groups — each with a GUID and URN key (`data_dictionary/`)
3. **Data Sheets:** Tabular outputs from the dictionary for populating asset databases
4. **IFC Model:** Open BIM exchange format enriched with property sets from the dictionary (`ifc/`)

## Key Conventions

- **Property keys:** `urn:demo:property:<snake_case_name>` — only lowercase letters, digits, underscores after the prefix
- **Object keys:** `urn:demo:object:<snake_case_name>`
- **GUIDs:** UUID4 format, e.g. `A1B2C3D4-E5F6-7890-ABCD-EF1234567890` — every entity must have a unique GUID
- **Display_Order:** Set to `0` when appending rows programmatically
- **Backups:** Scripts that modify data dictionary files must back up originals before writing

## Scripting Approach

Bash does not work in this environment. All automation is Python:

- Write scripts to `scripts/`
- Scripts write their outputs (`.txt`, `.csv`) to `outputs/`
- The user runs scripts manually and shares results

## QA/QC Rules

Defined in `qaqc/rules.md`. Active rules:
- **DD-01:** `Globally_unique_identifier` values in `PROPERTIES.csv` must be unique
- **DD-02:** `Property_key` values must match `^urn:demo:property:[a-z0-9_]+$`

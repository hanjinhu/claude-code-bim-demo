# BIM Data Dictionary — Demo Project

This is a simplified project demonstrating how Claude Code can accelerate BIM data dictionary development and quality assurance automation.

Demo sandbox for BIM data dictionary development and QA automation using Claude Code — Accenture AI Champion Network webinar, June 2026.

## Project Background

This project builds a **data dictionary** for underground utility assets — pipes, conduits, manholes, and related infrastructure. A data dictionary defines every object type, property, and rule needed to represent these assets consistently in BIM models and databases.

### The workflow has four stages:

Information Requirements → Data Dictionary → Data Sheets → IFC Model

- **Information Requirements (IR):** The client specifies what data needs
  to be captured for each asset type — property names, descriptions, and
  groupings called property sets.
- **Data Dictionary (DD):** We translate those requirements into a
  structured definition — objects, templates, properties, and groups —
  each with a unique identifier and standard key format.
- **Data Sheets:** Tabular outputs populated from the data dictionary,
  used to feed asset databases.
- **IFC Model:** The open BIM exchange format that consumes the data
  dictionary to enrich model elements with property sets.

## Repository Structure

```
├── README.md
├── docs/                        # Reference documents and background
├── information_requirements/    # Input: IR workbook from the client
├── data_dictionary/             # Output: parsed CSV files (generated)
├── qaqc/                        # QA rules to validate the dictionary
├── scripts/                     # Automation scripts (generated)
└── outputs/                     # Exploration and script outputs
```

## Domain

**Underground Utilities (UGU)** — the primary domain for this demo. Asset types include: Pipe, Conduit, Manhole, Valve.

## Key Conventions

- Property keys use URN format: `urn:demo:property:property_name`
- Object keys use URN format: `urn:demo:object:object_name`
- Every entity has a globally unique identifier (GUID)
- `Display_Order` is set to `0` when appending rows programmatically
- Scripts that modify data dictionary files must back up originals first
- Exploration scripts write output to `outputs/` as `.txt` files

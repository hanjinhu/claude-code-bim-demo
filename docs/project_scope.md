# Project Scope — BIM Data Dictionary (Demo)

## Background

This project delivers a data dictionary for underground utility assets
on behalf of a state transportation agency. The dictionary defines every
object type, property, and rule needed to represent underground utility
infrastructure consistently in BIM models and asset databases.

## Domains

This demo covers one domain: **Underground Utilities (UGU)**.
Asset types: Pipe, Conduit, Manhole, Valve.

## Deliverables

1. Data dictionary CSV files (objects, properties, property groups, templates)
2. QA/QC check scripts validating the dictionary against defined rules
3. Data sheets for database population
4. IFC model enriched with property sets from the dictionary

## Key Standards

- Property keys: URN format `urn:demo:property:<snake_case_name>`
- Object keys: URN format `urn:demo:object:<snake_case_name>`
- GUIDs: UUID4 format (e.g. `A1B2C3D4-E5F6-7890-ABCD-EF1234567890`)
- All entities must have a unique GUID
- Display_Order is set to 0 when appending rows programmatically

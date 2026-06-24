# Sandbox Build Guide

## Instructions for Claude Code — Demo Repo Setup

You are setting up a demo repository for a webinar about BIM data dictionary development. Your job is to build out the full sandbox structure: folders, reference documents, a dummy IR Excel workbook, QAQC rules, and a CLAUDE.md file. Follow every instruction below exactly.

---

## 1. Folder Structure

Ensure these folders exist (create if missing):

```
docs/
ifc/
information_requirements/
data_dictionary/
qaqc/
scripts/
scripts/outputs/
```

---

## 2. docs/project_scope.md

Create this file with the following content:

```markdown
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
```

---

## 3. information_requirements/IR_Demo.xlsx

Create an Excel workbook named `IR_Demo.xlsx` with exactly two sheets.

### Sheet 1: EIR-Elements

Row 1 is the header. Data starts at row 2.

| Category            | Element Name | Description                                                       | IFC Entity             |
| ------------------- | ------------ | ----------------------------------------------------------------- | ---------------------- |
| Underground Utility | Pipe         | A cylindrical conduit for conveying fluids or gases underground   | IfcPipeSegment         |
| Underground Utility | Conduit      | A protective tube enclosing electrical or communication cables    | IfcCableCarrierSegment |
| Underground Utility | Manhole      | An access chamber providing entry to underground utility networks | IfcChamberFacility     |
| Underground Utility | Valve        | A device controlling flow within a pipeline                       | IfcValve               |

### Sheet 2: EIR-Utility-Properties

Row 1 is the header. Data starts at row 2.

Columns (in this order):
`Category`, `Element Name`, `Property Set`, `Property Name`, `Description`, `Data Type`, `Allowed Values`

Data rows:

| Category            | Element Name | Property Set        | Property Name      | Description                                        | Data Type   | Allowed Values                                   |
| ------------------- | ------------ | ------------------- | ------------------ | -------------------------------------------------- | ----------- | ------------------------------------------------ |
| Underground Utility | Pipe         | General Features    | Utility Type       | The type of utility service the pipe carries       | Enumeration | Water; Gas; Electric; Telecom; Sewer; Irrigation |
| Underground Utility | Pipe         | General Features    | Owner              | The organisation responsible for the utility asset | String      |                                                  |
| Underground Utility | Pipe         | General Features    | Permit Number      | Permit number associated with the installation     | String      |                                                  |
| Underground Utility | Pipe         | Physical Properties | Material           | Primary material of the pipe                       | String      |                                                  |
| Underground Utility | Pipe         | Physical Properties | Diameter           | Internal diameter of the pipe in millimetres       | Real        |                                                  |
| Underground Utility | Pipe         | Physical Properties | Wall Thickness     | Thickness of the pipe wall in millimetres          | Real        |                                                  |
| Underground Utility | Pipe         | Location            | Installation Depth | Depth of the pipe below surface in metres          | Real        |                                                  |
| Underground Utility | Pipe         | Location            | GPS Coordinates    | GPS coordinates of the asset centroid              | String      |                                                  |
| Underground Utility | Conduit      | General Features    | Utility Type       | The type of utility service the conduit carries    | Enumeration | Electric; Telecom; Fiber Optic                   |
| Underground Utility | Conduit      | Physical Properties | Material           | Primary material of the conduit                    | String      |                                                  |

---

## 4. qaqc/rules.md

Create this file with the following content:

```markdown
# QA/QC Rules — Data Dictionary (Demo)

## Rule DD-01: GUID Uniqueness

**Description:** Every row in PROPERTIES.csv must have a unique value in the
`Globally_unique_identifier` column. No two properties may share the same GUID.

**Check:** Read PROPERTIES.csv. Find any duplicate values in the
`Globally_unique_identifier` column. Report each duplicate with the property
name and the offending GUID.

**Severity:** Error

---

## Rule DD-02: Property Key Format

**Description:** Every value in the `Property_key` column of PROPERTIES.csv
must follow the URN format: `urn:demo:property:<snake_case_name>` where
`<snake_case_name>` uses only lowercase letters, digits, and underscores.

**Check:** Read PROPERTIES.csv. Find any rows where `Property_key` does not
match the pattern `^urn:demo:property:[a-z0-9_]+$`. Report each violation
with the property name and the actual key value found.

**Severity:** Error
```

---

## 5. CLAUDE.md

Run `/init` to generate a CLAUDE.md for this project. After it is generated,
verify it includes:

- The four-stage pipeline: Information Requirements → Data Dictionary → Data Sheets → IFC Model
- The folder structure and what each folder contains
- The URN key format conventions
- The GUID format convention
- The rule that Display_Order is 0 when appending rows programmatically
- The outputs/ folder convention: exploration scripts write results here as .txt files

If any of these are missing, add them manually.

---

## 6. Verify

After completing all steps, confirm:

- [ ] `docs/project_scope.md` exists
- [ ] `information_requirements/IR_Demo.xlsx` exists with 2 sheets and correct data
- [ ] `qaqc/rules.md` exists with 2 rules
- [ ] `data_dictionary/`, `scripts/`, `outputs/`, `ifc/` folders exist (empty)
- [ ] `CLAUDE.md` exists and covers the conventions above

# Demo Prompts

## 1. Onboarding

```
Please read the README.md, docs/project_scope.md, and the CLAUDE.md file in this repo.
Then look at the folder structure — check what's in information_requirements/,
data_dictionary/template/, qaqc/, and ifc/sample_codes/.
When you're done, give me a brief summary: what is this project, what are the key
conventions I need to follow, and what are the three main tasks we'll be doing today.
```

---

## 2. Dev: IR → Data Dictionary

```
Read the information requirements workbook at
information_requirements/information_requirements.xlsx.
It has one sheet with four columns: Elements, Property Sets, Properties, Description.
Forward-fill the Elements and Property Sets columns where cells are blank — Excel
often leaves them empty when values carry over from the row above.

Then write a Python script under scripts/update/ that:
1. Makes a copy of each CSV in data_dictionary/template/ into data_dictionary/
2. Reads every row from the IR and adds the corresponding entries to:
   - data_dictionary/PROPERTIES_23386.csv (one row per unique property)
   - data_dictionary/PROPERTY_GROUPS_23386.csv (one row per unique property set)
   - data_dictionary/GROUP_PROPERTY_MEMBERSHIP.csv (linking properties to groups)
   - data_dictionary/OBJECTS_12006.csv (one row per unique element)

Follow the conventions in CLAUDE.md: URN key format urn:demo:property:<snake_case>,
Display_Order 0. Use data_dictionary/sample/ CSVs as a format reference —
but use urn:demo:... keys, not urn:caltrans:...

For every row added, generate a deterministic GUID using uuid5 derived from the
entity's URN key — not uuid4. Use a fixed project namespace so the same URN key
always produces the same GUID. Write the GUID to the Globally_unique_identifier
column for objects, property groups, and properties alike. Use the same GUIDs in
GROUP_PROPERTY_MEMBERSHIP.csv.

When reading or writing the template CSVs, use encoding="utf-8-sig" — the files
have an Excel BOM, and using plain utf-8 will silently corrupt the first column
header, leaving the Globally_unique_identifier column blank.

Save the script to scripts/update/ir_to_dd.py.
```

---

## 3. QA/QC

```
Read qaqc/qaqc_rules.md. It defines two rules:
- DD-01: all GUIDs in data_dictionary/PROPERTIES_23386.csv must be unique
- DD-02: all Property_key values must match urn:demo:property:<snake_case>

Write a Python script at scripts/qaqc/run_checks.py that checks both rules
against data_dictionary/PROPERTIES_23386.csv and writes a results summary to
outputs/qaqc_results.txt — listing any violations found, or confirming all checks passed.
```

**Fix prompt (after introducing the deliberate error):**

```
Fix the violation and re-run the check
```

---

## 4. IFC Model

```
Read the sample scripts in ifc/sample_codes/ to understand the ifcopenshell.api pattern for geometry and property sets.

Then write a Python script at scripts/ifc/create_pipe_model.py that:
1. Creates a new IFC4X3 model with SI units and a Body context
2. Adds one pipe segment named "Demo_Pipe_001" with a circular hollow profile:
   300 mm OD, 25 mm wall, 2 m long, along the X axis
3. Looks up the General Features property group (urn:demo:propertygroup:general_features)
   by joining PROPERTY_GROUPS_23386.csv → GROUP_PROPERTY_MEMBERSHIP.csv →
   PROPERTIES_23386.csv, and attaches those properties as "Pset_GeneralFeatures"
   with realistic values (UtilityType: Water, Owner: City Public Works Department,
   PermitNumber: UGU-2026-001)
4. Saves to outputs/demo_pipe_model.ifc

Two things to get right:
- Follow ifc_sample_code_3.py: model.create_entity for the profile,
  add_profile_representation + assign_representation + edit_object_placement
- Profile values go to create_entity in mm (model unit), so multiply metres by 1000.
  depth in add_profile_representation stays in metres — the API converts automatically.

Use encoding="utf-8-sig" for all CSV reads.
```

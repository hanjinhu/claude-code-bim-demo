#!/usr/bin/env python3
"""Populate data dictionary CSVs from the Information Requirements workbook.

Usage:
    python scripts/update/ir_to_dd.py

Reads:  information_requirements/information_requirements.xlsx
Writes: data_dictionary/PROPERTIES_23386.csv
        data_dictionary/PROPERTY_GROUPS_23386.csv
        data_dictionary/GROUP_PROPERTY_MEMBERSHIP.csv
        data_dictionary/OBJECTS_12006.csv
        data_dictionary/backup/*  (originals, if any existed)
"""

import csv
import re
import shutil
import uuid
from datetime import date
from pathlib import Path

import openpyxl

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IR_PATH = REPO_ROOT / "information_requirements" / "information_requirements.xlsx"
TEMPLATE_DIR = REPO_ROOT / "data_dictionary" / "template"
DD_DIR = REPO_ROOT / "data_dictionary"
BACKUP_DIR = DD_DIR / "backup"

TODAY = date.today().isoformat()

TEMPLATE_FILES = [
    "OBJECTS_12006.csv",
    "PROPERTIES_23386.csv",
    "PROPERTY_GROUPS_23386.csv",
    "GROUP_PROPERTY_MEMBERSHIP.csv",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def to_snake(name: str) -> str:
    """'Pipe Material' → 'pipe_material'  (only a-z, 0-9, _)"""
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip("_")


def to_camel(name: str) -> str:
    """'Pipe Material' → 'PipeMaterial'"""
    return "".join(w.capitalize() for w in re.split(r"\s+", name.strip()))


# Fixed namespace for this project — all GUIDs are derived from their URN key.
# uuid5 is deterministic: same URN key → same GUID every run, so re-running
# the script never invalidates GUIDs already referenced in IFC models.
_DD_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "urn:demo:")


def make_guid(urn_key: str) -> str:
    """Return an uppercase UUID5 derived from the entity's URN key.

    Format matches the sample data (e.g. 9E87A346-FDE1-44BD-A161-2361F7FE8E27).
    """
    return str(uuid.uuid5(_DD_NAMESPACE, urn_key)).upper()


# ---------------------------------------------------------------------------
# Step 1 – back up existing CSVs and copy fresh templates
# ---------------------------------------------------------------------------

def backup_and_copy_templates():
    BACKUP_DIR.mkdir(exist_ok=True)
    for fname in TEMPLATE_FILES:
        dest = DD_DIR / fname
        if dest.exists():
            backup_name = f"{Path(fname).stem}_backup_{TODAY}{Path(fname).suffix}"
            shutil.copy2(dest, BACKUP_DIR / backup_name)
            print(f"  Backed up  {fname}")
        shutil.copy2(TEMPLATE_DIR / fname, dest)
        print(f"  Copied     template/{fname} → data_dictionary/{fname}")


# ---------------------------------------------------------------------------
# Step 2 – read IR workbook
# ---------------------------------------------------------------------------

def read_ir():
    """Return list of row dicts.  Forward-fills Elements and Property Sets."""
    wb = openpyxl.load_workbook(IR_PATH, data_only=True)
    ws = wb.active

    header = None
    rows = []
    last_elem = ""
    last_pset = ""

    for raw in ws.iter_rows(values_only=True):
        if header is None:
            header = [str(c).strip() if c is not None else "" for c in raw]
            continue
        if not any(raw):
            continue

        rec = {
            col: (str(val).strip() if val is not None else "")
            for col, val in zip(header, raw)
        }

        # Forward-fill merged / blank cells
        elem = rec.get("Elements", "")
        pset = rec.get("Property Sets", "")
        if elem:
            last_elem = elem
        else:
            rec["Elements"] = last_elem
        if pset:
            last_pset = pset
        else:
            rec["Property Sets"] = last_pset

        rows.append(rec)

    return rows


# ---------------------------------------------------------------------------
# Step 3 – build entity dicts from IR rows
# ---------------------------------------------------------------------------

def build_entities(ir_rows):
    objects = {}     # snake_key → {guid, name, key}
    groups = {}      # snake_key → {guid, name, key}
    properties = {}  # snake_key → {guid, name, description, key,
                     #               first_group_guid, ir_alignment}
    memberships = [] # list of (grp_guid, grp_key, prop_guid, prop_key)

    for row in ir_rows:
        elem = row.get("Elements", "").strip()
        pset = row.get("Property Sets", "").strip()
        prop = row.get("Properties", "").strip()
        desc = row.get("Description", "").strip()

        if not prop:
            continue  # need at least a property name to do anything

        # Object
        if elem:
            obj_snake = to_snake(elem)
            obj_key = f"urn:demo:object:{obj_snake}"
            if obj_snake not in objects:
                objects[obj_snake] = {
                    "guid": make_guid(obj_key),
                    "name": elem,
                    "key": obj_key,
                }

        # Property group
        if pset:
            grp_snake = to_snake(pset)
            grp_key = f"urn:demo:propertygroup:{grp_snake}"
            if grp_snake not in groups:
                groups[grp_snake] = {
                    "guid": make_guid(grp_key),
                    "name": pset,
                    "key": grp_key,
                }
            grp_info = groups[grp_snake]
        else:
            grp_info = None

        # Property (deduplicated by snake key; first occurrence wins)
        prop_snake = to_snake(prop)
        prop_key = f"urn:demo:property:{prop_snake}"
        if prop_snake not in properties:
            properties[prop_snake] = {
                "guid": make_guid(prop_key),
                "name": prop,
                "description": desc,
                "key": prop_key,
                "first_group_guid": grp_info["guid"] if grp_info else "",
                "ir_alignment": f"{elem}/{pset}" if (elem and pset) else (elem or pset),
            }

        # Membership link
        if grp_info:
            memberships.append((
                grp_info["guid"],
                grp_info["key"],
                properties[prop_snake]["guid"],
                properties[prop_snake]["key"],
            ))

    # Deduplicate memberships (same group+property pair may appear if IR has
    # repeated rows)
    seen = set()
    unique_memberships = []
    for m in memberships:
        key = (m[0], m[2])
        if key not in seen:
            seen.add(key)
            unique_memberships.append(m)

    return objects, groups, properties, unique_memberships


# ---------------------------------------------------------------------------
# Step 4 – write CSVs
# ---------------------------------------------------------------------------

def _read_headers(path: Path):
    # utf-8-sig strips the BOM that Excel adds, so column names are clean ASCII
    with open(path, newline="", encoding="utf-8-sig") as f:
        return next(csv.reader(f))


def _write_csv(path: Path, headers, rows):
    """Overwrite file with header row + data rows (drops template blank rows)."""
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_objects(objects):
    dest = DD_DIR / "OBJECTS_12006.csv"
    headers = _read_headers(dest)
    rows = []
    for info in objects.values():
        row = {h: "" for h in headers}
        row["Globally_unique_identifier"] = info["guid"]
        row["Object_Key"] = info["key"]
        row["Object_Name"] = info["name"]
        row["Object_Status"] = "Draft"
        row["Information_Requirements"] = info["name"]
        row["IFC_Entity"] = "IfcDistributionSystem"
        row["IFC_Predefined_Type"] = "NOTDEFINED"
        row["IFC_Schema_Version"] = "IFC4x3_ADD2"
        row["OmniClass_Table"] = "N/A"
        row["OmniClass_Code"] = "N/A"
        row["AASHTOWare_Pay_Item"] = "TBD"
        row["Schema_Version"] = "1"
        rows.append(row)
    _write_csv(dest, headers, rows)
    print(f"  Wrote {len(rows)} objects       → {dest.name}")


def write_groups(groups):
    dest = DD_DIR / "PROPERTY_GROUPS_23386.csv"
    headers = _read_headers(dest)
    rows = []
    for info in groups.values():
        row = {h: "" for h in headers}
        row["Globally_unique_identifier"] = info["guid"]
        row["Group_key"] = info["key"]
        row["Names_in_language_N"] = f"{to_camel(info['name'])} | en-EN"
        row["Definitions_in_language_N"] = info["name"]
        row["Status"] = "Draft"
        row["Date_of_creation"] = TODAY
        row["Date_of_last_change"] = "N/A"
        row["Date_of_revision"] = "N/A"
        row["Date_of_version"] = TODAY
        row["Version_number"] = "1"
        row["Revision_number"] = "N/A"
        row["Creators_language"] = "en-EN"
        row["Country_of_use"] = "US"
        row["Category_of_group_of_properties"] = "Class"
        rows.append(row)
    _write_csv(dest, headers, rows)
    print(f"  Wrote {len(rows)} property groups → {dest.name}")


def write_properties(properties):
    dest = DD_DIR / "PROPERTIES_23386.csv"
    headers = _read_headers(dest)
    rows = []
    for info in properties.values():
        row = {h: "" for h in headers}
        row["Globally_unique_identifier"] = info["guid"]
        row["Property_key"] = info["key"]
        row["Names_in_language_N"] = f"{to_camel(info['name'])} | en-EN"
        row["Definitions_in_language_N"] = info["name"]
        row["Units"] = "unitless"
        row["Descriptions_in_language_N"] = info["description"]
        row["Physical_quantity"] = "without"
        row["Method_of_measurement"] = "N/A"
        row["Data_type"] = "String"
        row["Status"] = "Active"
        row["Date_of_creation"] = TODAY
        row["Date_of_revision"] = "N/A"
        row["Date_of_version"] = TODAY
        row["Version_number"] = "1"
        row["Revision_number"] = "N/A"
        row["Creators_language"] = "en-EN"
        if info["first_group_guid"]:
            row["Groups_of_properties"] = f"({info['first_group_guid']})"
        row["Country_of_use"] = "US"
        row["Country_of_origin"] = "US"
        row["IR_Property_Alignment"] = info["ir_alignment"]
        rows.append(row)
    _write_csv(dest, headers, rows)
    print(f"  Wrote {len(rows)} properties    → {dest.name}")


def write_memberships(memberships):
    dest = DD_DIR / "GROUP_PROPERTY_MEMBERSHIP.csv"
    with open(dest, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Group_GUID", "Group_Key", "Property_GUID", "Property_Key"])
        for row in memberships:
            writer.writerow(row)
    print(f"  Wrote {len(memberships)} memberships   → {dest.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n--- Step 1: Backup and copy templates ---")
    backup_and_copy_templates()

    print("\n--- Step 2: Read IR workbook ---")
    ir_rows = read_ir()
    print(f"  Read {len(ir_rows)} data rows from {IR_PATH.name}")

    print("\n--- Step 3: Build entities ---")
    objects, groups, properties, memberships = build_entities(ir_rows)
    print(f"  {len(objects)} unique objects")
    print(f"  {len(groups)} unique property groups")
    print(f"  {len(properties)} unique properties")
    print(f"  {len(memberships)} group-property memberships")

    print("\n--- Step 4: Write CSVs ---")
    write_objects(objects)
    write_groups(groups)
    write_properties(properties)
    write_memberships(memberships)

    print("\nDone.")


if __name__ == "__main__":
    main()

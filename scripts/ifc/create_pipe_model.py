#!/usr/bin/env python3
"""Create a demo IFC model containing one IfcPipeSegment enriched with
Pset_GeneralFeatures properties drawn from the data dictionary.

Pipe geometry assumptions:
  - Outer diameter : 300 mm  (PIPE_OUTER_RADIUS = 0.15 m)
  - Wall thickness : 25 mm   (PIPE_WALL_THICKNESS = 0.025 m)
  - Length         : 6 m     (PIPE_LENGTH = 6.0 m)
  - Orientation    : along the Z axis, origin at (0, 0, 0)
Adjust the constants below if different dimensions are needed.

Usage:
    python scripts/ifc/create_pipe_model.py

Reads:  data_dictionary/PROPERTY_GROUPS_23386.csv
        data_dictionary/GROUP_PROPERTY_MEMBERSHIP.csv
        data_dictionary/PROPERTIES_23386.csv
Writes: outputs/demo_pipe_model.ifc
"""

import csv
from pathlib import Path

import ifcopenshell
import ifcopenshell.api.root
import ifcopenshell.api.unit
import ifcopenshell.api.context
import ifcopenshell.api.geometry
import ifcopenshell.api.aggregate
import ifcopenshell.api.spatial
import ifcopenshell.api.pset

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DD_DIR = REPO_ROOT / "data_dictionary"
OUTPUT_IFC = REPO_ROOT / "outputs" / "demo_pipe_model.ifc"

PSET_NAME = "Pset_GeneralFeatures"
GROUP_KEY = "urn:demo:propertygroup:general_features"

PIPE_OUTER_RADIUS = 0.15    # metres (300 mm OD)
PIPE_WALL_THICKNESS = 0.025  # metres (25 mm wall)
PIPE_LENGTH = 2.0            # metres (2000 mm)

# Demo values for Pset_GeneralFeatures — keyed by the CamelCase display name
# produced from Names_in_language_N (e.g. "UtilityType | en-EN" → "UtilityType")
PROPERTY_VALUES = {
    "UtilityType":   "Water",
    "Owner":         "City Public Works Department",
    "PermitNumber":  "UGU-2026-001",
}


# ---------------------------------------------------------------------------
# Data dictionary helpers
# ---------------------------------------------------------------------------

def _load_csv(path: Path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def get_general_features_properties():
    """Return the CamelCase display names of all properties in the General
    Features group, in the order they appear in PROPERTIES_23386.csv."""

    # Step 1 — find the group GUID
    groups = _load_csv(DD_DIR / "PROPERTY_GROUPS_23386.csv")
    group_guid = next(
        (r["Globally_unique_identifier"].strip()
         for r in groups
         if r.get("Group_key", "").strip() == GROUP_KEY),
        None,
    )
    if not group_guid:
        print(f"  Warning: group '{GROUP_KEY}' not found in PROPERTY_GROUPS csv")
        return []

    # Step 2 — collect property GUIDs that belong to this group
    memberships = _load_csv(DD_DIR / "GROUP_PROPERTY_MEMBERSHIP.csv")
    prop_guids = {
        r["Property_GUID"].strip()
        for r in memberships
        if r.get("Group_GUID", "").strip() == group_guid
    }
    if not prop_guids:
        print(f"  Warning: no properties found for group GUID {group_guid!r}")
        return []

    # Step 3 — resolve display names from PROPERTIES csv
    # Names_in_language_N is "PipeMaterial | en-EN" — strip the language tag
    props = _load_csv(DD_DIR / "PROPERTIES_23386.csv")
    names = []
    for row in props:
        if row.get("Globally_unique_identifier", "").strip() in prop_guids:
            raw = row.get("Names_in_language_N", "").strip()
            name = raw.split(" | ")[0] if " | " in raw else raw
            if name:
                names.append(name)
    return names


# ---------------------------------------------------------------------------
# IFC model builder
# ---------------------------------------------------------------------------

def build_project_skeleton():
    """Return (model, site, body_context) for a fresh IFC4X3 file."""
    model = ifcopenshell.file(schema="IFC4X3_ADD2")

    project = ifcopenshell.api.root.create_entity(
        model, ifc_class="IfcProject", name="UGU Demo Project"
    )
    ifcopenshell.api.unit.assign_unit(model)  # default SI units

    # Geometry contexts — required so viewers can locate the representation
    model_ctx = ifcopenshell.api.context.add_context(model, context_type="Model")
    body_ctx = ifcopenshell.api.context.add_context(
        model,
        context_type="Model",
        context_identifier="Body",
        target_view="MODEL_VIEW",
        parent=model_ctx,
    )

    site = ifcopenshell.api.root.create_entity(
        model, ifc_class="IfcSite", name="Demo Site"
    )
    ifcopenshell.api.aggregate.assign_object(
        model, relating_object=project, products=[site]
    )

    return model, site, body_ctx


def add_pipe_geometry(model, pipe, body_ctx):
    """Attach a straight circular hollow extrusion to the pipe element.

    Follows the ifc_sample_code_3.py pattern:
      model.create_entity  →  add_profile_representation  →  assign_representation
    This lets ifcopenshell handle tessellation of the curved profile correctly,
    avoiding the segmented-circle artifact that appears with manual entity wiring.
    """
    # Profile: circular hollow cross-section using model.create_entity (not createIfc*)
    # The model unit is mm (set by assign_unit), so profile values must be in mm.
    # add_profile_representation converts depth from SI (m) to mm automatically,
    # but model.create_entity writes raw values with no conversion — hence * 1000.
    profile = model.create_entity(
        "IfcCircleHollowProfileDef",
        ProfileType="AREA",
        ProfileName="PipeProfile",
        Radius=PIPE_OUTER_RADIUS * 1000,          # m → mm
        WallThickness=PIPE_WALL_THICKNESS * 1000,  # m → mm
    )

    # Placement at origin (default identity matrix)
    ifcopenshell.api.geometry.edit_object_placement(model, product=pipe)

    # Let the API build the solid + shape representation correctly
    representation = ifcopenshell.api.geometry.add_profile_representation(
        model, context=body_ctx, profile=profile, depth=PIPE_LENGTH
    )

    # Assign representation via API (not direct attribute assignment)
    ifcopenshell.api.geometry.assign_representation(
        model, product=pipe, representation=representation
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUTPUT_IFC.parent.mkdir(exist_ok=True)

    print("Reading General Features properties from data dictionary...")
    prop_names = get_general_features_properties()
    if not prop_names:
        print("No properties found — run scripts/update/ir_to_dd.py first.")
        return
    print(f"  {len(prop_names)} properties: {', '.join(prop_names)}")

    print("\nBuilding IFC model...")
    model, site, body_ctx = build_project_skeleton()

    # Create the pipe element
    pipe = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcPipeSegment",
        predefined_type="RIGIDSEGMENT",
        name="Demo_Pipe_001",
    )
    add_pipe_geometry(model, pipe, body_ctx)
    ifcopenshell.api.spatial.assign_container(
        model, relating_structure=site, products=[pipe]
    )
    print(
        f"  Created IfcPipeSegment '{pipe.Name}'  "
        f"({PIPE_OUTER_RADIUS * 2 * 1000:.0f} mm OD, {PIPE_LENGTH:.0f} m long)"
    )

    # Attach Pset_GeneralFeatures with demo values
    pset = ifcopenshell.api.pset.add_pset(model, product=pipe, name=PSET_NAME)
    prop_values = {name: PROPERTY_VALUES.get(name, "N/A") for name in prop_names}
    ifcopenshell.api.pset.edit_pset(model, pset=pset, properties=prop_values)
    for name, val in prop_values.items():
        print(f"    {name}: {val}")
    print(f"  Attached '{PSET_NAME}' with {len(prop_names)} properties")

    model.write(str(OUTPUT_IFC))
    print(f"\nSaved → {OUTPUT_IFC.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

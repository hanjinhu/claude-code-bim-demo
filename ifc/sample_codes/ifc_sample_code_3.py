import ifcopenshell.api.root
import ifcopenshell.api.unit
import ifcopenshell.api.context
import ifcopenshell.api.project
import ifcopenshell.api.geometry

# Let's create a new project using millimeters with a single furniture element at the origin.
model = ifcopenshell.api.project.create_file
ifcopenshell.api.root.create_entity(model, ifc_class="IfcProject")
ifcopenshell.api.unit.assign_unit(model)

# We want our representation to be the 3D body of the element.
# This representation context is only created once per project.
# You must reuse the same body context every time you create a new representation.
model3d = ifcopenshell.api.context.add_context(model, context_type="Model")
body = ifcopenshell.api.context.add_context(model,
    context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=model3d)

# Create our element with an object placement.
element = ifcopenshell.api.root.create_entity(model, ifc_class="IfcFurniture")
ifcopenshell.api.geometry.edit_object_placement(model, product=element)

# Hollow circular profiles are typically used for steel members
# profile = model.create_entity("IfcCircleProfileDef", ProfileName="300C", ProfileType="AREA",
#     Radius=300)
profile = model.create_entity("IfcCircleHollowProfileDef", ProfileName="300CHS", ProfileType="AREA",
    Radius=150, WallThickness=5)

# Let's create our representation!
# A profile-based representation, 1 meter long
representation = ifcopenshell.api.geometry.add_profile_representation(model, context=body, profile=profile, depth=1)

# Assign our new body representation back to our element
ifcopenshell.api.geometry.assign_representation(model, product=element, representation=representation)
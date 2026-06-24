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

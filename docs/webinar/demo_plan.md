# Webinar Demo Plan

**Event:** Claude Code: Real-World Use Cases and Lessons Learned
**Date:** June 26, 2026, 2:30 to 3:30 pm ET
**Audience:** Accenture AI Champion Network — engineers and PMs, mixed technical levels
**Goal:** Show real results, make Claude Code feel accessible and worth trying
**Duration:** 12 minutes

---

## Narrative

> "A complex, domain-specific project that would take days of manual Excel work — automated in hours, without writing a single line of code."

**Mindset framing (say this early):**

> "I stopped thinking of Claude as a tool and started treating it like an engineer on my team. I'm the project lead — I understand the domain, I set the direction. Claude is the engineer — it does the implementation. Just like a real engineer, it needs to be onboarded. You have to give it context. You have to answer its questions. When you do that investment up front, it works independently and respects your standards without being reminded every time."

---

## Demo Arc

| Time         | Segment                               | What to Show                                                                                                                                            | Why It Lands                                                           |
| ------------ | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| 0:00–1:30   | **The problem**                 | Pipeline slide → open real Caltrans IR Excel (`sample/`) → open real DD Excel → mention 47-rule QA review                                          | Audience feels the complexity before you solve it                      |
| 1:30–2:00   | **Sandbox transition**          | Switch to the sandbox repo — explain why: production data is confidential, don't want to risk live edits; sandbox is downloadable for the audience     | Sets up credibility: this is based on real work, not a toy example     |
| 2:00–4:00   | **Teaching Claude the project** | Ask Claude to read the repo files and summarize; run`/init` to generate CLAUDE.md; scroll through it                                                  | Key insight:*invest once in context, Claude remembers every session* |
| 4:00–6:30   | **Dev: IR → Data Dictionary**  | Claude reads IR Excel, writes a script to copy template CSVs to`data_dictionary/` and populate them; show the populated CSV                           | Shows Claude respects*your* conventions, not generic ones            |
| 6:30–9:00   | **QA/QC automation**            | Claude writes check scripts from`qaqc/qaqc_rules.md`; deliberately introduce an error; script catches it; Claude fixes it and re-runs clean           | Non-developers: you don't need to read code to get value               |
| 9:00–11:00  | **IFC model**                   | Claude reads`ifc/sample_codes/`, writes a script that creates a pipe model with property sets from the data dictionary; show the output `.ifc` file | Full pipeline payoff: the dictionary isn't just a spreadsheet          |
| 11:00–12:00 | **One takeaway**                | "I didn't teach it Python. I taught it my project."                                                                                                     | Memorable, repeatable message for the network                          |

---

## Segment Scripts

### 0:00–1:30 — The Problem

**Screen:**

1. Show pipeline slide: *Information Requirements → Data Dictionary → Data Sheets → IFC Model*
2. Open `information_requirements/sample/InformationRequirements_06232026.xlsx` — scroll through a properties sheet
3. Open `data_dictionary/sample/Data Dictionary_UGU.xlsx` — scroll sheet tabs, open `PROPERTIES_23386` to show row and column volume
4. Show `qaqc/sample/Caltrans Data Dictionary QAQC Process v3_2.pdf` briefly — this is the review document from the client

**Script:**

> "I'm going to show you something I've been working on for a real client project. The overall workflow looks like this. [show slide] We start with an **information requirements document** — the client telling us what data they need to capture for every underground utility asset: pipes, conduits, manholes, valves. That drives the **data dictionary**, which is the structured definition of every object, property, and rule. The dictionary then feeds two outputs: **data sheets** used to populate an asset database, and **IFC models** — the open format used for exchanging BIM data.
>
> [open IR Excel] This is the information requirements workbook — each row is a property the client needs. [open DD Excel] This is the data dictionary we're building from it — about a dozen interconnected sheets, hundreds of properties, strict rules about how everything links. [show QA PDF] And this is the QA review we received from the client — 47 rules we have to check the dictionary against before delivery.
>
> Managing all of this manually — keeping the dictionary in sync with the requirements, catching errors across sheets — is exactly the kind of work that takes days and is easy to get wrong."

---

### 1:30–2:00 — Sandbox Transition

**Script:**

> "Now — I'm not going to demo live on the production repo. There's real client data in there, and I don't want to risk making unintended changes in front of an audience.
>
> So I built a sandbox version. Same structure, same conventions, simpler data — four asset types, a handful of properties. It's available for you to download after this session if you want to try it yourself. Everything I'm about to show you works exactly the same way on the real project — I've done it."

**Transition:** *"Let me start by teaching Claude what this project is."*

---

### 2:00–4:00 — Teaching Claude the Project

**Screen:**

1. Show VS Code Explorer — point out folder structure
2. Open Claude Code chat panel — paste the onboarding prompt
3. Show Claude reading through files and producing a summary
4. Run `/init` — show `CLAUDE.md` being generated
5. Scroll through `CLAUDE.md`: pipeline, folder conventions, URN key format, GUID format, Display_Order rule

**Onboarding prompt (paste this):**

```
Please read the README.md, docs/project_scope.md, and the CLAUDE.md file in this repo.
Then look at the folder structure — check what's in information_requirements/,
data_dictionary/template/, qaqc/, and ifc/sample_codes/.
When you're done, give me a brief summary: what is this project, what are the key
conventions I need to follow, and what are the three main tasks we'll be doing today.
```

**Script:**

> "The first thing I did was organize the project and give Claude a tour. I collected all the documents — requirements, reference files, QA rules — into one repo with clear folders. Then I ran `/init` [show command] — that's a built-in Claude Code command that reads the codebase and generates this file. [open CLAUDE.md]
>
> CLAUDE.md is the briefing document — it persists across every session. Claude knows the pipeline, the naming conventions, which folders to write to, even the rule about Display_Order. I didn't type all of this — Claude drafted it from reading the repo. I corrected it. One investment; every task after this is faster."

**Key insight to land:**

> "Think of it like onboarding a new engineer. You'd walk them through the project, explain the conventions, answer their questions. Claude needs the same thing. The difference is you only do it once."

**Transition:** *"Now let's put that understanding to work."*

---

### 4:00–6:30 — Dev: IR → Data Dictionary

**Screen:**

1. Open `information_requirements/information_requirements.xlsx` — point out the columns (Elements, Property Sets, Properties, Description)
2. Paste the dev prompt into Claude Code chat
3. Watch Claude read the IR, write the script under `scripts/update/`, run it
4. Open `data_dictionary/PROPERTIES_23386.csv` — show the populated rows with correct GUIDs, URN keys, and formatting

**Dev prompt (paste this):**

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

**Script:**

> "The workflow is: the client updates their requirements document, I need to reflect those changes in the data dictionary. [show IR] Here's the IR — properties, their descriptions, the property sets they belong to. [paste prompt]
>
> I'm not writing code. I'm describing the task the way I'd describe it to an engineer: what the input is, what needs to happen, what conventions to follow. [watch Claude work]
>
> [open populated CSV] There it is — correct GUIDs, correct URN keys, linked to the right property groups. Zero manual work after that prompt."

**Transition:** *"Now let's make sure everything is consistent."*

---

### 6:30–9:00 — QA/QC

**Screen:**

1. Open `qaqc/qaqc_rules.md` — show the two rules (DD-01: GUID uniqueness, DD-02: key format)
2. Paste the QA/QC prompt
3. Watch Claude write `scripts/qaqc/run_checks.py`
4. Run script — show clean results
5. Manually edit one row in `PROPERTIES_23386.csv`: change a property key to `urn:demo:property:Utility Type` (space instead of underscore)
6. Re-run — show DD-02 violation caught
7. Ask Claude to fix it — show it corrects the key and re-runs clean

**QA/QC prompt (paste this):**

```
Read qaqc/qaqc_rules.md. It defines two rules:
- DD-01: all GUIDs in data_dictionary/PROPERTIES_23386.csv must be unique
- DD-02: all Property_key values must match urn:demo:property:<snake_case>

Write a Python script at scripts/qaqc/run_checks.py that checks both rules
against data_dictionary/PROPERTIES_23386.csv and writes a results summary to
outputs/qaqc_results.txt — listing any violations found, or confirming all checks passed.
```

**Deliberate error to introduce (between runs):**

- Open `data_dictionary/PROPERTIES_23386.csv`
- Find any `Property_key` value and change it to include a space, e.g. `urn:demo:property:Utility Type`
- Re-run the QA/QC script → DD-02 violation appears in `outputs/qaqc_results.txt`
- Ask Claude: *"Fix the violation and re-run the check"*

**Script:**

> "The client gave us a QA review with 47 rules. I've distilled two of them here. [open qaqc_rules.md] Rule DD-01: no duplicate GUIDs. DD-02: every property key must follow the URN format. [paste prompt, watch Claude write the script, run it] Clean.
>
> Now let me introduce a mistake — something that's easy to miss manually. [edit the CSV] I've just changed a property key to have a space in it. [re-run] There it is — DD-02 violation, tells me exactly which row and what the problem is. [ask Claude to fix it, re-run] Clean again.
>
> This is the iteration loop: write → check → fix → re-check. Claude handles all three."

**Transition:** *"Last step — the model."*

---

### 9:00–11:00 — IFC Model

**Screen:**

1. Open `ifc/sample_codes/ifc_roadway_hierarchy_update_caltrans.py` briefly — point out the ifcopenshell pattern
2. Paste the IFC prompt
3. Watch Claude write `scripts/ifc/create_pipe_model.py`
4. User runs the script
5. Show `outputs/demo_pipe_model.ifc` exists; optionally open in a viewer

**IFC prompt (paste this):**

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

**Script:**

> "IFC is the open standard that BIM models are exchanged in — it's the end product the data dictionary feeds. [show sample code briefly] The sample scripts I've included show how to work with IFC using Python. [paste prompt, watch Claude write the script]
>
> [user runs the script] The model file is there. The property set is attached. The data dictionary defined the properties — the IFC model consumes them. That's the full pipeline: requirements in, model out."

---

### 11:00–12:00 — Takeaway

**Script:**

> "Let me recap what just happened. We started with a client's requirements document — plain Excel. Claude read it, understood the structure, and built the data dictionary from it. It checked its own work against the QA rules. And it produced an IFC model ready for exchange.
>
> I didn't teach Claude Python. I taught it my project. The CLAUDE.md, the organized folders, the README — that's where the value lives. Every session after that investment, Claude works like someone who already knows the codebase.
>
> That's the shift: stop thinking about what Claude can do in general. Start thinking about what it can do *in your project*, once it knows it."

---

## Lessons Learned (say these in the CLAUDE.md segment)

- **Bash doesn't always work.** In some environments, Claude can't run shell commands. Workaround: ask Claude to write a Python script that saves output to `outputs/` as a text file, then read that file. Slower, but reliable — and leaves a record of every exploration step.
- **Organize before you prompt.** Folders, README, CLAUDE.md pay off on every task after.
- **Onboard like a new team member.** Let it read, let it ask questions, let it summarize its understanding. Front-loaded investment.
- **Pre-write demo prompts.** Typing live under pressure introduces typos. Paste from a prepared file.

---

## Pre-Written Prompts (ready to paste)

All four prompts are written out in the segment scripts above. Copy them from there.

---

## Next Steps Before Demo Day

- [ ] Run `scripts/explore/inspect_ir.py` to verify dummy IR content is suitable
- [ ] Confirm `openpyxl` and `ifcopenshell` are installed in the demo environment
- [ ] Do a full dry run: run all three segments end-to-end in a test chat session
- [ ] Pre-stage the deliberate error row in the CSV (or practice making it live — it's fast)
- [ ] Build 1–2 intro slides: pipeline diagram + one-liner on project context

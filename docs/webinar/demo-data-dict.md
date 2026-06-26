# Webinar Demo Plan

**Event:** Claude Code: Real-World Use Cases and Lessons Learned
**Date:** June 26, 2026, 2:30 to 3:30 pm ET
**Audience:** Accenture AI Champion Network — engineers and PMs, mixed technical levels
**Goal:** Show real results, make Claude Code feel accessible and worth trying
**Duration:** 12 minutes

---

## Narrative

> "A complex, domain-specific project that would take days of manual Excel work — automated in hours, without writing a single line of code."

**Mindset framing (say this at the start of the 2:00–4:00 segment):**

> "I don't treat Claude Code as a tool. I treat it as a co-worker. Like an intern who helps me with tasks.
>
> When I give a task to an intern, I do three things.
>
> One — I tell them the project context. The big picture. Where the finish line is. What the deliverables are. That's *context engineering*.
>
> Two — I give them specific requirements for the task. What the input is. What the output should be. What rules to follow. That's *prompt engineering*.
>
> Three — I give them examples to follow. Never zero-shot. Show them what good looks like.
>
> Same with Claude. Context, requirements, examples. That's the recipe."

---

## Demo Arc

| Time         | Segment                               | What to Show                                                                                                                                                                    | Why It Lands                                                           |
| ------------ | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| 0:00–0:30   | **Sandbox up front**            | Explain: production has client data I can't show; this is a sandbox with the same structure, downloadable for the audience                                                      | Sets the constraint up front — no real client data on screen          |
| 0:30–2:00   | **The problem**                 | Pipeline slide → open sandbox IR workbook → open`data_dictionary/template/` → show `qaqc/qaqc_rules.md`. Mention real project has hundreds of properties and 47 QA rules | Audience feels the complexity before you solve it                      |
| 2:00–4:00   | **Teaching Claude the project** | Ask Claude to read the repo files and summarize; run`/init` to generate CLAUDE.md; scroll through it                                                                          | Key insight:*invest once in context, Claude remembers every session* |
| 4:00–6:30   | **Dev: IR → Data Dictionary**  | Claude reads IR Excel, writes a script to copy template CSVs to`data_dictionary/` and populate them; show the populated CSV                                                   | Shows Claude respects*your* conventions, not generic ones            |
| 6:30–9:00   | **QA/QC automation**            | Claude writes check scripts from`qaqc/qaqc_rules.md`; deliberately introduce an error; script catches it; Claude fixes it and re-runs clean                                   | Non-developers: you don't need to read code to get value               |
| 9:00–11:00  | **IFC model**                   | Claude reads`ifc/sample_codes/`, writes a script that creates a pipe model with property sets from the data dictionary; show the output `.ifc` file                         | Full pipeline payoff: the dictionary isn't just a spreadsheet          |
| 11:00–12:00 | **One takeaway**                | "I didn't teach it Python. I taught it my project."                                                                                                                             | Memorable, repeatable message for the network                          |

---

## Segment Scripts

### 0:00–0:30 — Sandbox up front

**Screen:**

1. Show VS Code with the sandbox repo open in the Explorer

**Script:**

> "Quick note before I start. My demo today is based on a real client project. The production repo has client data I can't show on screen. Plus, I don't want to mess up the production repo. So I created a sandbox.
>
> Same structure. Same conventions. Just simpler dummy data. You can download it after this session and play with it.
>
> Everything I'm about to show works the same way on the real project."

---

### 0:30–2:00 — The Problem

**Screen:**

1. Briefly return to the pipeline slide as a recap visual (already shown at the very start of the demo)
2. Open `information_requirements/information_requirements.xlsx` — scroll through the sheet, point out the columns
3. Open `data_dictionary/template/` — show the empty CSV templates that need to be populated
4. Open `qaqc/qaqc_rules.md` — show the two distilled rules

**Script:**

> "To recap the pipeline. Information requirements from the client come in as an Excel workbook. Based on them, I will create a data dictionary to define the objects and properties. Finally I need to create an IFC model based on the data dictionary.
>
> [open IR Excel] This is the requirements workbook. Each row is a property the client needs. The sandbox has four asset types and a handful of properties. The real project has hundreds of properties across a dozen sheets.
>
> [open template folder] This is the data dictionary template. Four CSVs we need to populate. Objects — one row per asset type, like a pipe or a manhole. Properties — one row per property, like diameter or material. Property Groups — bundles of related properties, like General Features. And a membership file that links properties to their groups. Each row needs a unique ID. Each property has to link to the right group. Strict rules about how everything connects.
>
> [open qaqc_rules.md] And this is the QA review. Two rules here. The real project has nearly 50 rules.
>
> Doing all of this by hand takes days. You have to keep the dictionary in sync with the requirements. You have to catch errors across many sheets. Easy to get wrong."

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

**Mindset framing (say this first, before the screen demo):**

> "Quick thing before I start. I don't treat Claude Code as a tool. I treat it as a co-worker. Like an intern who helps me with tasks.
>
> When I give a task to an intern, I do three things.
>
> One — I tell them the project context. The big picture. Where the finish line is. What the deliverables are. That's like *context engineering*.
>
> Two — I give them specific requirements for the task. What the input is. What the output should be. What rules to follow. That's like *prompt engineering*.
>
> Three — I give them examples to follow. Never do zero-shot. Show them what a good output looks like.
>
> Same with Claude. Context, requirements, examples. That's the recipe. The rest of this demo is me doing those three things."

**Script:**

> "The first thing is to help claude understand the project. I collected all the documents, such as requirements, reference files, QA rules and put them into one repo with clear folder structure. I also drafted a README.md with the project background, the four-stage workflow, the folder layout, and the key conventions — just the initial context I'd want any new team member to read first. [open README.md] Then I ran `/init` [show command] — that's a built-in Claude Code command that reads the codebase, including the README, and generates this file. [open CLAUDE.md]
>
> CLAUDE.md is the briefing document. Whenever you open Claude Code, it will read this file first. That is a way to keep the memory. Claude now knows the project. I just need to check it and maybe make some edits, just to make sure we are on the same page. One time setup. Every task after this is faster."

**One quick tip before we start working:**

> "Just like `/init`, Claude Code has other built-in commands. Let me show you an important one.
>
> When I learned to drive, before I learned how to move a car, I had to learn how to stop one. Same idea here. When a prompt goes wrong, I type `/rewind`. That undoes Claude's last step and go back to the last checkpoint. Then I try again with a better prompt.
>
> It is good to learn this one early."

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

> "Now let's build the data dictionary from scratch. The client gives me the information requirements. I need to turn them into the four CSV files. [show IR] Here's the IR. Properties, descriptions, and the property sets they belong to.
>
> If I did this by hand, here is what I would do. Start from the empty templates. Copy them into the data dictionary folder. Then fill them in row by row from the IR. Now Claude Code will do it for me. It will create a new GUID for every object, every property group, every property. It will make sure every key is in the right format. And it will build the membership file that links properties to groups. [paste prompt]
>
> I'm not writing code. I'm describing the task the way I'd describe it to an engineer. What the input is. What the output should be. What rules to follow. [watch Claude work]
>
> [open populated CSV] There it is. Correct GUIDs. Correct URN keys. Linked to the right property groups. Zero manual work after that prompt."

**Transition:** *"Next step. Let's review the output and run QA/QC on it."*

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

> "OK, so the client gave us a QA review with 47 rules. I picked two of them for the demo. [open qaqc_rules.md] Rule DD-01 — no duplicate GUIDs. Rule DD-02 — every property key has to follow the URN format. Let's have Claude write a checker for both. [paste prompt, watch Claude write the script, run it] Clean. All good.
>
> Now let's break something on purpose. Something that's easy to miss by eye. [edit the CSV] I just changed a property key to have a space in it. Let's re-run the check. [re-run] There it is. DD-02 violation. It tells me exactly which row, and what the problem is. Now let's ask Claude to fix it. [ask Claude to fix it, re-run] Clean again.
>
> This is the loop. Write. Check. Fix. Re-check. Claude handles all three."

**Transition:** *"OK, last step — let's build the model."*

---

### 9:00–11:00 — IFC Model

**Screen:**

1. Open the `ifc/sample_codes/` folder — show the three Python files (`ifc_sample_code_1.py`, `ifc_sample_code_2.py`, `ifc_sample_code_3.py`). Briefly open one or two to show the `ifcopenshell` pattern
2. Paste the IFC prompt
3. Watch Claude write `scripts/ifc/create_pipe_model.py`
4. User runs the script
5. Show `outputs/demo_pipe_model.ifc` exists; optionally open in a viewer
6. Run `/context` — show the bar; mention `/compact` as the next step when it fills up

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

> "OK, last step. Let's build the IFC model. IFC is the open standard for BIM. IFC models are the end product for digital delivery projects — like the one we did for PennDOT, the first digital delivery project in the US bridge industry. It's what the data sheets feed into.
>
> Now, writing Python code to generate IFC takes special skills. So I want to give Claude some examples to follow. [open `ifc/sample_codes/` folder] I put three Python files in here. They all use a library called `ifcopenshell` to create IFC models. [open one file] This one is from the official `ifcopenshell` documentation. [open another] These two are from my previous projects. I use these files to teach Claude how to write IFC code. Remember the recipe — context, requirements, examples. This is the examples part. [paste prompt, watch Claude work]
>
> [user runs the script] And there's the model. The property set is attached. The data dictionary defined the properties. The IFC model consumes them. That's the full pipeline. Requirements in. Model out."

**One more tip before the takeaway:**

> "We just did three big tasks in one session. Let me show you one more thing. [run `/context`] This shows me how full the conversation window is. When it gets close to full, I run `/compact`. That summarizes everything so far, so I can keep going without losing the thread. Good one to know when you're working on a long task."

---

### 11:00–12:00 — Takeaway

**Script:**

> "Let me quickly recap what we just did. We started with the client's requirements — just a plain Excel file. Claude read it. It understood the structure. It built the data dictionary from it. Then it checked its own work against the QA rules. And it produced an IFC model, ready to share.
>
> Here's the thing. I didn't teach Claude Python. I taught it my project. The CLAUDE.md, the organized folders, the README — that's where the value is. Every session after that investment, Claude works like someone who already knows the codebase.
>
> So that's the shift. Stop thinking about what Claude can do in general. Start thinking about what it can do *in your project*, once it knows it."

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
- [X] Confirm `openpyxl` and `ifcopenshell` are installed in the demo environment
- [ ] Do a full dry run: run all three segments end-to-end in a test chat session
- [ ] Pre-stage the deliberate error row in the CSV (or practice making it live — it's fast)
- [X] Build 1–2 intro slides: pipeline diagram + one-liner on project context

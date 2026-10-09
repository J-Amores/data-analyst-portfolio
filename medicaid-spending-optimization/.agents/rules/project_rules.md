### RUNTIME & ENVIRONMENT CONSTRAINTS
- An isolated Python virtual environment is located inside the project folder at ./.venv.
- NEVER install packages globally and NEVER call system python or pip.
- For all shell executions, package installations, testing, and script runs, you MUST either:
  1. Prefix commands using the project binary: ./.venv/bin/python ... and ./.venv/bin/pip ...
  2. Or explicitly activate the environment in every subshell: source .venv/bin/activate && <command>
- Verify with which python before executing scripts to ensure the path resolves to medicaid-spend-optimization/.venv/bin/python.

### MANDATORY GOVERNING DOCUMENTS
- docs/PROJECT_CHARTER.md (Business problem, READY framework, North Star metric, 3 hypotheses)
- docs/DATA_SPEC.md (Physical schema, CLEAN framework rules, data grain)
- docs/AGENT_TASKS.md (Sequential task backlog)
- docs/HIRING_MANAGER_CRITIQUE.md (Executive standards & newsflash visualization rules)

### NEGATIVE CONSTRAINTS
- NEVER sum Tot_Spndng_* across raw tables without filtering out Mftr_Name == 'Overall'.
- NEVER impute missing cells resulting from CMS HIPAA suppression (<11 claims) with zero or mean values; keep as NaN/NULL.
- Keep data processing and statistical algorithms in src/ modular scripts; do not generate unorganized notebook dumps.
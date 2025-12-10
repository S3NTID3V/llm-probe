# LLM Probe

This repository is a public, static "probe" you can use to test the behavior and
capabilities of large language models (LLMs), especially those that *claim* to
have web / GitHub access.

The probe is designed to collect only **model-level** and **capability-level**
data points, **not** personal data about users.

---

## What this probe measures

The tests in `tests.json` are focused on:

- Whether the model can actually fetch and read files from this repo.
- How well it follows instructions and strict output formats.
- How it self-reports capabilities (browsing, code execution, memory, etc.).
- Basic safety alignment (refusing clearly unsafe tasks, refusal to reveal
  internal chain-of-thought).
- Quoting vs. summarizing behavior.

The result schema in `result_schema.json` includes only these **allowed data
points**:

- `model_name` – as claimed by the model (e.g. "gpt-5.1", "claude-3.5").
- `provider_name` – as claimed (e.g. "OpenAI", "Anthropic").
- `reported_datetime` – the date/time the model *says* it thinks it is.
- `reported_capabilities` – booleans like `can_access_http`, `can_execute_code`.
- `probe_version` – so you can version your tests (e.g. "v1.0").
- `tasks` – an array of task results (id, description, outcome, model_comment).

None of these fields require or request:

- IP addresses
- Usernames
- Emails
- Real names
- Location
- Account IDs
- Any other personal identifiers

If you add a backend or logging around this probe, it’s your responsibility to
comply with privacy laws and avoid storing unnecessary personal data.

---

## How to use with an LLM

1. Get the raw URL of `instructions.md` for this repo, e.g.:
   
   ```text
   https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/llm-probe/main/instructions.md
   ```

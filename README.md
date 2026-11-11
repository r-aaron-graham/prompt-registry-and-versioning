# Prompt Registry and Versioning

This repository contains a simple prompt registry and versioning service.  It allows you to
store, retrieve, and manage prompts used for large language model (LLM) queries.  Each prompt
is versioned automatically, enabling you to track changes over time and experiment with
different versions.

## Features

* Lightweight SQLite database for persistent storage of prompts.
* Command‑line interface (CLI) built with `click` to add, list, update, and retrieve prompts.
* Automatic version incrementing when prompts are updated.
* Ability to tag prompts with arbitrary metadata (e.g. description, owner, tags).

## Usage

Install dependencies and run the CLI:

```bash
pip install -r requirements.txt
python cli.py --help
```

### Version a prompt

Run this example with a fresh local `prompts.db`. The first command returns
the row ID. Use that ID in the update command if it differs from `1`.

```bash
python cli.py add summarize "Summarize this document" --description "Document summary" --tags summarization
python cli.py update 1 "Summarize the article and list its key points"
python cli.py list
python cli.py get summarize --version 1
python cli.py get summarize --version 2
```

The list shows version 2. Both versions remain retrievable by name, with their
original text preserved. A missing prompt or row ID reports an error and exits
with a nonzero status.

## Extending the registry

The registry is intentionally simple.  You can extend it by adding new commands to `cli.py` or
by importing the `PromptRegistry` class in your own scripts.
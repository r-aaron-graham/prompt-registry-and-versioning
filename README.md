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

### Adding a new prompt

```bash
python cli.py add "Summarize this document" --description "Generic summarization prompt" --tags summarization,default
```

### Listing prompts

```bash
python cli.py list
```

### Updating a prompt

```bash
python cli.py update 1 "Summarize the following article and highlight key points"
```

### Retrieving a prompt by name and version

```bash
python cli.py get "Summarize this document" --version 2
```

## Extending the registry

The registry is intentionally simple.  You can extend it by adding new commands to `cli.py` or
by importing the `PromptRegistry` class in your own scripts.
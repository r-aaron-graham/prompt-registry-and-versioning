"""Prompt registry implementation using SQLite.

This module defines the `Prompt` data model and the `PromptRegistry` class, which provides
methods to add, update, list, and retrieve prompts.  It uses the built‑in `sqlite3` module
for simplicity and does not require any external database server.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass
class Prompt:
    """Represent a registered prompt."""

    id: int
    name: str
    version: int
    text: str
    description: Optional[str] = None
    tags: Optional[str] = None


class PromptRegistry:
    """Registry for storing prompts and their versions."""

    def __init__(self, db_path: Path | str = "prompts.db") -> None:
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        """Create the prompts table if it does not already exist."""
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                version INTEGER NOT NULL,
                text TEXT NOT NULL,
                description TEXT,
                tags TEXT
            );
            """
        )
        self.conn.commit()

    def add_prompt(self, name: str, text: str, description: Optional[str] = None, tags: Optional[str] = None) -> Prompt:
        """Append the next version for a prompt name."""
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO prompts (name, version, text, description, tags) "
                "SELECT ?, COALESCE(MAX(version), 0) + 1, ?, ?, ? "
                "FROM prompts WHERE name = ?",
                (name, text, description, tags, name),
            )
            row = self.conn.execute(
                "SELECT id, name, version, text, description, tags FROM prompts WHERE id = ?",
                (cur.lastrowid,),
            ).fetchone()
        return Prompt(*row)

    def update_prompt(self, prompt_id: int, new_text: str) -> Prompt:
        """Update an existing prompt by creating a new version entry with the updated text."""
        cur = self.conn.cursor()
        cur.execute("SELECT name, description, tags FROM prompts WHERE id = ?", (prompt_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Prompt ID {prompt_id} not found")
        name, description, tags = row
        return self.add_prompt(name, new_text, description, tags)

    def list_prompts(self) -> Iterable[Prompt]:
        """Return all prompts with their latest versions."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT p1.id, p1.name, p1.version, p1.text, p1.description, p1.tags "
            "FROM prompts p1 "
            "JOIN (SELECT name, MAX(version) AS max_version FROM prompts GROUP BY name) p2 "
            "ON p1.name = p2.name AND p1.version = p2.max_version "
            "ORDER BY p1.name"
        )
        rows = cur.fetchall()
        for row in rows:
            yield Prompt(*row)

    def get_prompt(self, name: str, version: Optional[int] = None) -> Prompt:
        """Retrieve a prompt by name.  If version is None, return the latest version."""
        cur = self.conn.cursor()
        if version is None:
            cur.execute(
                "SELECT id, name, version, text, description, tags FROM prompts WHERE name = ? ORDER BY version DESC LIMIT 1",
                (name,),
            )
        else:
            cur.execute(
                "SELECT id, name, version, text, description, tags FROM prompts WHERE name = ? AND version = ?",
                (name, version),
            )
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Prompt '{name}' with version '{version or 'latest'}' not found")
        return Prompt(*row)

    def close(self) -> None:
        """Close the underlying database connection."""
        self.conn.close()
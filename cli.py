"""Command‑line interface for the prompt registry.

This CLI allows you to add, list, update, and retrieve prompts from the registry.  It uses the
`PromptRegistry` class defined in the `prompt_registry` package.  Run `python cli.py --help`
for usage instructions.
"""

from __future__ import annotations

import click
from prompt_registry import PromptRegistry


def get_registry(ctx: click.Context) -> PromptRegistry:
    """Retrieve a PromptRegistry instance from the context or create one."""
    registry = ctx.obj.get("registry")
    if registry is None:
        registry = PromptRegistry()
        ctx.obj["registry"] = registry
        ctx.call_on_close(registry.close)
    return registry


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Prompt registry CLI.  Manage your LLM prompts with versioning."""
    ctx.obj = ctx.obj or {}


@cli.command(help="Add a new prompt or create a new version of an existing prompt")
@click.argument("name")
@click.argument("text")
@click.option("--description", default=None, help="Optional description of the prompt")
@click.option("--tags", default=None, help="Comma‑separated tags for categorization")
@click.pass_context
def add(ctx: click.Context, name: str, text: str, description: str, tags: str) -> None:
    registry = get_registry(ctx)
    prompt = registry.add_prompt(name, text, description, tags)
    click.echo(f"Added prompt '{prompt.name}' version {prompt.version} (id={prompt.id})")


@cli.command("list", help="List all prompts and their latest versions")
@click.pass_context
def list_prompts(ctx: click.Context) -> None:
    registry = get_registry(ctx)
    prompts = list(registry.list_prompts())
    if not prompts:
        click.echo("No prompts found.")
        return
    for prompt in prompts:
        click.echo(f"[{prompt.id}] {prompt.name} (v{prompt.version}): {prompt.description or ''}")


@cli.command(help="Update an existing prompt by id, creating a new version")
@click.argument("prompt_id", type=int)
@click.argument("text")
@click.pass_context
def update(ctx: click.Context, prompt_id: int, text: str) -> None:
    registry = get_registry(ctx)
    try:
        prompt = registry.update_prompt(prompt_id, text)
        click.echo(f"Updated prompt '{prompt.name}' to version {prompt.version}")
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


@cli.command(help="Retrieve a prompt by name and optionally version")
@click.argument("name")
@click.option("--version", type=int, default=None, help="Version number to retrieve (defaults to latest)")
@click.pass_context
def get(ctx: click.Context, name: str, version: int | None) -> None:  # noqa: A003
    registry = get_registry(ctx)
    try:
        prompt = registry.get_prompt(name, version)
        click.echo(f"Prompt '{prompt.name}' (v{prompt.version})\n{prompt.text}")
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


if __name__ == "__main__":
    cli()
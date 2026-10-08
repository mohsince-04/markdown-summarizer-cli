from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel

from llm_service import generate_summary, ask_question

app = typer.Typer(help="Smart Local CLI Summarizer & Search Tool")
console = Console()


def load_markdown_files(path: Path) -> str:
    if not path.exists():
        console.print(f"[bold red]Error:[/bold red] Path '{path}' does not exist.")
        raise typer.Exit(code=1)

    combined_text = ""
    if path.is_file():
        combined_text = path.read_text(encoding="utf-8")
    elif path.is_dir():
        md_files = list(path.glob("**/*.md")) + list(path.glob("**/*.markdown"))
        if not md_files:
            console.print(
                f"[bold red]Error:[/bold red] No Markdown files found in '{path}'."
            )
            raise typer.Exit(code=1)
        for file in md_files:
            combined_text += f"\n\n--- File: {file.name} ---\n\n" + file.read_text(
                encoding="utf-8"
            )

    return combined_text


@app.command()
def summarize(
    path: Path = typer.Argument(..., help="Path to markdown file or directory")
):
    """Summarize a file or folder of Markdown files."""
    with console.status("[bold green]Analyzing content with Gemini...[/bold green]"):
        content = load_markdown_files(path)
        summary = generate_summary(content)

    console.print(
        Panel(f"[bold blue]{summary.title}[/bold blue]", title="Document Summary")
    )
    console.print(f"\n[bold]Overview:[/bold] {summary.one_sentence_summary}\n")
    console.print("[bold]Key Takeaways:[/bold]")
    for point in summary.key_takeaways:
        console.print(f"• {point}")
    console.print(f"\n[bold]Topics:[/bold] [dim]{', '.join(summary.topics)}[/dim]\n")


@app.command()
def ask(
    path: Path = typer.Argument(..., help="Path to markdown file or directory"),
    query: str = typer.Option(..., "-q", "--query", help="Question to ask"),
):
    """Ask a question about local markdown files."""
    with console.status("[bold green]Searching context...[/bold green]"):
        content = load_markdown_files(path)
        result = ask_question(content, query)

    console.print(
        Panel(
            f"[bold]Question:[/bold] {result.question}\n\n{result.answer}",
            title="Q&A Result",
        )
    )
    console.print(f"[bold]Confidence:[/bold] {result.confidence_score * 100:.0f}%")
    if result.relevant_quotes:
        console.print("\n[bold]Relevant Quotes:[/bold]")
        for quote in result.relevant_quotes:
            console.print(f'> [italic]"{quote}"[/italic]')


if __name__ == "__main__":
    app()

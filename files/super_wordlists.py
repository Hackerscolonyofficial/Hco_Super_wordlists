import itertools
import sys
import time
import shutil
import os
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.prompt import Prompt

# Create Console
console = Console()

# Character Mapping for Patterns
CHAR_MAP = {
    "?l": "abcdefghijklmnopqrstuvwxyz",
    "?u": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "?d": "0123456789",
    "?s": "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
}

# Get Terminal Height
def get_terminal_height():
    return shutil.get_terminal_size((80, 20)).lines

# Print Progress Bar at Bottom
def print_progress(count, total, speed):
    height = get_terminal_height()
    sys.stdout.write(f"\033[{height};0H")  # Move cursor to bottom line
    sys.stdout.write(f"[cyan][Progress][/cyan] [red]{count}/{total}[/red] [blue]| Speed: [green]{speed:.2f} words/sec[/green]\n")
    sys.stdout.flush()

# Convert Pattern to Charset
def parse_pattern(pattern):
    for key, value in CHAR_MAP.items():
        pattern = pattern.replace(key, value)
    return pattern

# Generate Sentence-Based Wordlist
def generate_sentence_wordlist(words, min_words, max_words, output_file):
    try:
        total_combinations = sum(
            len(list(itertools.combinations(words, length))) for length in range(min_words, max_words + 1)
        )
        console.print(Panel(f"[cyan]Generating {total_combinations} sentence-based words...[/]", title="[bold yellow]📜 Sentence-Based Wordlist Generator[/]"))

        count = 0
        start_time = time.time()
        with Progress() as progress:
            task = progress.add_task("[green]Generating Words...", total=total_combinations)
            f = open(output_file, "w") if output_file else sys.stdout
            for length in range(min_words, max_words + 1):
                for combo in itertools.combinations(words, length):
                    variations = {
                        "".join(combo),  
                        " ".join(combo),  
                        "".join(combo).lower(),  
                        "".join(combo).upper(),  
                        "".join(w.capitalize() for w in combo)  
                    }
                    for variant in variations:
                        f.write(variant + "\n")
                        count += 1
                        progress.update(task, advance=1)

            if output_file:
                f.close()

        total_time = time.time() - start_time
        console.print(Panel(f"[green]✔ Sentence-Based Wordlist Generation Completed in [bold red]{total_time:.2f} seconds![/][/]", title="[bold cyan]✅ Completed![/]"))

    except KeyboardInterrupt:
        console.print(Panel("[red]❌ Process Stopped by User![/]", title="⚠ [yellow]Warning[/]"))

# Generate Brute-Force Wordlist
def generate_wordlist(charset, min_length, max_length, output_file):
    try:
        total_words = sum(len(charset) ** length for length in range(min_length, max_length + 1))
        console.print(Panel(f"[cyan]Generating {total_words} words...[/]", title="[bold yellow]💥 Brute-Force Wordlist Generator[/]"))

        count = 0
        start_time = time.time()
        with Progress() as progress:
            task = progress.add_task("[green]Generating Words...", total=total_words)
            f = open(output_file, "w") if output_file else sys.stdout
            for length in range(min_length, max_length + 1):
                for word in itertools.product(charset, repeat=length):
                    f.write(''.join(word) + "\n")
                    count += 1
                    progress.update(task, advance=1)

            if output_file:
                f.close()

        total_time = time.time() - start_time
        console.print(Panel(f"[green]✔ Wordlist Generation Completed in [bold blue]{total_time:.2f} seconds![/][/]", title="[bold cyan]✅ Completed![/]"))

    except KeyboardInterrupt:
        console.print(Panel("[red]❌ Process Stopped by User![/]", title="⚠ [yellow]Warning[/]"))

# Main Function
if __name__ == "__main__":
    console.print(Panel("[bold magenta]🔥 PyCrunch++ - Advanced Wordlist Generator 🔥[/]", title="[bold cyan]🎉 Welcome to PyCrunch++[/]"))

    console.print(Panel(
        "[bold yellow]1️⃣ Brute-force wordlist (character set)[/]\n"
        "[bold magenta]2️⃣ Sentence-based wordlist (words)[/]", 
        title="[bold cyan]📌 Select Mode[/]"
    ))

    mode = Prompt.ask("[yellow]Enter your choice (1/2)[/]", choices=["1", "2"])
    
    if mode == "1":
        console.print(Panel("[bold blue]🔢 Brute-Force Wordlist Mode[/]", title="[bold cyan]💡 Info[/]"))
        min_length = int(Prompt.ask("[yellow]Enter minimum length[/]"))
        max_length = int(Prompt.ask("[yellow]Enter maximum length[/]"))
        charset = Prompt.ask("[yellow]Enter character set (e.g., abc123!@# or ?l?u?d for pattern mode)[/]")
        output_file = Prompt.ask("[yellow]Enter output file name (leave empty for terminal output)[/]", default=None)

        if any(x in charset for x in CHAR_MAP):
            charset = parse_pattern(charset)

        generate_wordlist(charset, min_length, max_length, output_file)

    elif mode == "2":
        console.print(Panel("[bold magenta]📜 Sentence-Based Wordlist Mode[/]", title="[bold cyan]💡 Info[/]"))
        words = Prompt.ask("[magenta]Enter words (comma separated, e.g., sudip,gorai,007,python)[/]").split(",")
        min_words = int(Prompt.ask("[magenta]Enter minimum words in combination[/]"))
        max_words = int(Prompt.ask("[magenta]Enter maximum words in combination[/]"))
        output_file = Prompt.ask("[magenta]Enter output file name (leave empty for terminal output)[/]", default=None)

        generate_sentence_wordlist(words, min_words, max_words, output_file)

    else:
        console.print(Panel("[red]❌ Invalid option! Please choose 1 or 2.[/]", title="⚠ [yellow]Error[/]"))
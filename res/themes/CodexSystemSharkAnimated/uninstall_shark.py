from pathlib import Path
import shutil
import sys

MARKER_START = "    # >>> CODEX SHARK OVERLAY >>>"
MARKER_END = "    # <<< CODEX SHARK OVERLAY <<<"

def find_repo():
    if len(sys.argv) > 1:
        p = Path(sys.argv[1]).resolve()
        if (p / "main.py").exists():
            return p

    default = Path(r"C:\TuringScreen\turing-smart-screen-python")
    if (default / "main.py").exists():
        return default

    raise SystemExit("Repositorio nao encontrado.")

repo = find_repo()
main_py = repo / "main.py"

text = main_py.read_text(encoding="utf-8")
start = text.find(MARKER_START)
if start >= 0:
    end = text.find(MARKER_END, start)
    if end >= 0:
        end = text.find("\n", end)
        end = len(text) if end < 0 else end + 1
        if start > 0 and text[start-1:start] == "\n":
            start -= 1
        text = text[:start] + text[end:]
        main_py.write_text(text, encoding="utf-8", newline="\n")
        print("Integracao removida de main.py.")

for p in [
    repo / "codex_shark.py",
    repo / "res" / "codex_shark",
    repo / "res" / "themes" / "CodexSystemSharkAnimated",
]:
    if p.is_file():
        p.unlink()
        print(f"Removido: {p}")
    elif p.is_dir():
        shutil.rmtree(p)
        print(f"Removido: {p}")

print("Codex Shark Animated removido.")

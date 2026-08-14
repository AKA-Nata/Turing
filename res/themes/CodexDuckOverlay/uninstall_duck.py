from pathlib import Path
import shutil
import sys

MARKER_START = "    # >>> CODEX DUCK OVERLAY >>>"
MARKER_END = "    # <<< CODEX DUCK OVERLAY <<<"

def find_repo_root() -> Path:
    if len(sys.argv) > 1:
        p = Path(sys.argv[1]).resolve()
        if (p / "main.py").exists():
            return p
    default = Path(r"C:\TuringScreen\turing-smart-screen-python")
    if (default / "main.py").exists():
        return default
    p = Path.cwd()
    if (p / "main.py").exists():
        return p
    raise SystemExit("Repositorio nao encontrado.")

repo = find_repo_root()
main_py = repo / "main.py"
text = main_py.read_text(encoding="utf-8")

start = text.find(MARKER_START)
if start >= 0:
    end = text.find(MARKER_END, start)
    if end >= 0:
        end = text.find("\n", end)
        if end < 0:
            end = len(text)
        else:
            end += 1

        # Remove one optional blank line left by the patch.
        if start > 0 and text[start-1:start] == "\n":
            start -= 1

        text = text[:start] + text[end:]
        main_py.write_text(text, encoding="utf-8", newline="\n")
        print("Integracao removida de main.py.")

module = repo / "codex_duck.py"
if module.exists():
    module.unlink()
    print("codex_duck.py removido.")

assets = repo / "res" / "codex_duck"
if assets.exists():
    shutil.rmtree(assets)
    print("Sprites removidos.")

print("Codex Duck removido.")

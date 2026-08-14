from pathlib import Path
import shutil
import sys

PACK_DIR = Path(__file__).resolve().parent
MARKER_START = "    # >>> CODEX DUCK OVERLAY >>>"
MARKER_END = "    # <<< CODEX DUCK OVERLAY <<<"

PATCH = """    # >>> CODEX DUCK OVERLAY >>>
    try:
        from codex_duck import start_duck_overlay
        start_duck_overlay()
    except Exception as e:
        logger.warning("Codex Duck could not start: %s" % str(e))
    # <<< CODEX DUCK OVERLAY <<<
"""


def find_repo_root() -> Path:
    # 1) Explicit argument
    if len(sys.argv) > 1:
        p = Path(sys.argv[1]).resolve()
        if (p / "main.py").exists() and (p / "library").is_dir():
            return p

    # 2) Package extracted inside repository
    for p in [PACK_DIR, PACK_DIR.parent, Path.cwd()]:
        if (p / "main.py").exists() and (p / "library").is_dir():
            return p

    # 3) User's known installation path
    default = Path(r"C:\TuringScreen\turing-smart-screen-python")
    if (default / "main.py").exists():
        return default

    raise SystemExit(
        "Repositorio nao encontrado.\n"
        "Execute: python install_duck.py C:\\TuringScreen\\turing-smart-screen-python"
    )


repo = find_repo_root()
main_py = repo / "main.py"
target_module = repo / "codex_duck.py"
target_assets = repo / "res" / "codex_duck"
backup = repo / "main.py.before_codex_duck"

text = main_py.read_text(encoding="utf-8")

if MARKER_START not in text:
    anchor = "    scheduler.PingStats(); time.sleep(0.25)\n"
    if anchor not in text:
        raise SystemExit(
            "Nao encontrei o ponto de integracao esperado em main.py.\n"
            "Nenhuma alteracao foi feita."
        )

    if not backup.exists():
        shutil.copy2(main_py, backup)

    text = text.replace(anchor, anchor + "\n" + PATCH, 1)
    main_py.write_text(text, encoding="utf-8", newline="\n")
    print("main.py integrado com Codex Duck.")
else:
    print("main.py ja possui a integracao Codex Duck; patch ignorado.")

shutil.copy2(PACK_DIR / "codex_duck.py", target_module)
target_assets.mkdir(parents=True, exist_ok=True)

for src in (PACK_DIR / "assets").glob("duck_*.png"):
    shutil.copy2(src, target_assets / src.name)

print(f"Modulo : {target_module}")
print(f"Sprites: {target_assets}")
print(f"Backup : {backup}")
print()
print("Instalacao concluida.")
print("Agora execute o monitor normalmente como Administrador:")
print(f"  cd {repo}")
print("  python main.py")

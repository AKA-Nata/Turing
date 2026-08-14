from pathlib import Path
import shutil
import sys

PACK = Path(__file__).resolve().parent
MARKER_START = "    # >>> CODEX DINO OVERLAY >>>"
MARKER_END = "    # <<< CODEX DINO OVERLAY <<<"

PATCH = """    # >>> CODEX DINO OVERLAY >>>
    try:
        from codex_dino import start_dino_overlay
        start_dino_overlay()
    except Exception as e:
        logger.warning("Codex Dino could not start: %s" % str(e))
    # <<< CODEX DINO OVERLAY <<<
"""

def find_repo():
    if len(sys.argv) > 1:
        p = Path(sys.argv[1]).resolve()
        if (p / "main.py").exists() and (p / "library").is_dir():
            return p

    default = Path(r"C:\TuringScreen\turing-smart-screen-python")
    if (default / "main.py").exists():
        return default

    p = Path.cwd()
    if (p / "main.py").exists() and (p / "library").is_dir():
        return p

    raise SystemExit(
        "Repositorio nao encontrado.\n"
        "Use: python install_dino.py C:\\TuringScreen\\turing-smart-screen-python"
    )

def same_path(a: Path, b: Path) -> bool:
    try:
        return a.resolve() == b.resolve()
    except Exception:
        return str(a).lower() == str(b).lower()

repo = find_repo()

src_theme = PACK / "theme" / "CodexSystemDinoAnimated"
dst_theme = repo / "res" / "themes" / "CodexSystemDinoAnimated"

if not src_theme.exists():
    raise SystemExit(
        f"Tema-fonte nao encontrado em: {src_theme}\n"
        "Extraia o ZIP completo preservando as subpastas."
    )

# Se o pacote foi extraido DENTRO da propria pasta final do tema,
# nao tentamos apagar o diretorio corrente (Windows gera WinError 32).
if same_path(PACK, dst_theme):
    print("Pacote executado dentro da pasta final do tema.")
    print("Modo seguro: copiando arquivos do tema sem remover o diretorio atual.")
    dst_theme.mkdir(parents=True, exist_ok=True)
    for src in src_theme.iterdir():
        dst = dst_theme / src.name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
else:
    if dst_theme.exists():
        shutil.rmtree(dst_theme)
    shutil.copytree(src_theme, dst_theme)

# Runtime module/assets
shutil.copy2(PACK / "overlay" / "codex_dino.py", repo / "codex_dino.py")

dst_assets = repo / "res" / "codex_dino"
dst_assets.mkdir(parents=True, exist_ok=True)
for src in (PACK / "overlay" / "assets").glob("dino_*.png"):
    shutil.copy2(src, dst_assets / src.name)

# Patch main.py
main_py = repo / "main.py"
backup = repo / "main.py.before_codex_dino"
text = main_py.read_text(encoding="utf-8")

if MARKER_START not in text:
    anchor = "    scheduler.PingStats(); time.sleep(0.25)\n"
    if anchor not in text:
        raise SystemExit(
            "Ponto de integracao nao encontrado em main.py. "
            "Tema e assets foram copiados, mas main.py nao foi alterado."
        )

    if not backup.exists():
        shutil.copy2(main_py, backup)

    text = text.replace(anchor, anchor + "\n" + PATCH, 1)
    main_py.write_text(text, encoding="utf-8", newline="\n")
    print("main.py integrado com Codex Dino.")
else:
    print("main.py ja possui integracao Codex Dino.")

print()
print("Instalacao concluida.")
print(f"Tema   : {dst_theme}")
print(f"Modulo : {repo / 'codex_dino.py'}")
print(f"Sprites: {dst_assets}")
print(f"Backup : {backup}")
print()
print("Agora execute:")
print(f"  cd {repo}")
print("  python configure.py")
print()
print("Selecione Theme = CodexSystemDinoAnimated")
print("Depois Save and run.")

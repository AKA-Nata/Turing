CODEX SYSTEM GATOR ANIMATED
==========================

Conteudo
--------
- Tema completo CodexSystemGatorAnimated
- Jacare pixel-art animado
- Interacoes:
  1) anda para a direita
  2) para e pisca/observa
  3) anda para a esquerda
  4) para e abre/fecha a boca
  5) dorme
  6) repete o ciclo
- Preview GIF
- Instalador
- Desinstalador

Compatibilidade preparada
-------------------------
- Turing Smart Screen 3.5"
- 480x320 landscape
- turing-smart-screen-python
- Windows
- mesma fila serial do monitor principal

INSTALACAO
----------
1. Feche o Turing System Monitor.

2. Extraia este ZIP.

3. Abra PowerShell como Administrador.

4. Entre na pasta extraida e rode:

   python install_gator.py C:\TuringScreen\turing-smart-screen-python

5. Depois:

   cd C:\TuringScreen\turing-smart-screen-python
   python configure.py

6. Selecione:
   Theme: CodexSystemGatorAnimated
   Hardware monitoring: Automatic / LibreHardwareMonitor
   Ethernet interface: Ethernet

7. Save and run.

COMPORTAMENTO
-------------
Padrao:
- FPS = 3.0
- STEP_PX = 6
- TRACK_X_MIN = 96
- TRACK_X_MAX = 352
- TRACK_Y = 264
- IDLE_SECONDS = 6
- CHOMP_SECONDS = 6
- SLEEP_SECONDS = 18

Para alterar:
C:\TuringScreen\turing-smart-screen-python\codex_gator.py

OBSERVACAO
----------
O instalador ja tenta parar automaticamente a instancia anterior do
turing-smart-screen-python antes de copiar os arquivos e aplicar o patch.

DESINSTALAR
-----------
python uninstall_gator.py C:\TuringScreen\turing-smart-screen-python

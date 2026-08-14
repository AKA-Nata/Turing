CODEX SYSTEM COW ANIMATED
========================

Conteudo
--------
- Tema completo CodexSystemCowAnimated
- Vaca pixel-art animada
- Interacoes:
  1) anda da esquerda para a direita
  2) para e come grama
  3) anda da direita para a esquerda
  4) para e dorme
  5) repete o ciclo
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

   python install_cow.py C:\TuringScreen\turing-smart-screen-python

5. Depois:

   cd C:\TuringScreen\turing-smart-screen-python
   python configure.py

6. Selecione:
   Theme: CodexSystemCowAnimated
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
- TRACK_Y = 266
- GRAZE_SECONDS = 8
- SLEEP_SECONDS = 30

Para alterar:
C:\TuringScreen\turing-smart-screen-python\codex_cow.py

DESINSTALAR
-----------
python uninstall_cow.py C:\TuringScreen\turing-smart-screen-python

OBSERVACAO
----------
O overlay usa a mesma instancia do display e a mesma fila serial do
turing-smart-screen-python. Ele nao tenta abrir a COM5 separadamente.

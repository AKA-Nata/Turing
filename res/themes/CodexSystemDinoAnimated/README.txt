CODEX SYSTEM DINO ANIMATED
==========================

Conteudo
--------
- Tema completo CodexSystemDinoAnimated
- Dinossauro pixel-art animado
- 4 frames para cada direcao
- Preview GIF
- Instalador
- Desinstalador

Compatibilidade preparada
-------------------------
- Turing Smart Screen 3.5"
- 480x320 landscape
- turing-smart-screen-python
- Windows
- CodexSystemDinoAnimated
- mesma fila serial do monitor principal

INSTALACAO
----------
1. Feche o Turing System Monitor.

2. Extraia este ZIP.

3. Abra PowerShell como Administrador.

4. Entre na pasta extraida e rode:

   python install_dino.py C:\TuringScreen\turing-smart-screen-python

5. Depois:

   cd C:\TuringScreen\turing-smart-screen-python
   python configure.py

6. Selecione:

   Theme: CodexSystemDinoAnimated
   Hardware monitoring: Automatic / LibreHardwareMonitor
   Ethernet interface: Ethernet

7. Save and run.

ANIMACAO
--------
Padrao:
- 3 FPS
- passo 6 px
- x=96 ate 352
- y=277
- vai para a direita e volta para a esquerda

Para alterar:
C:\TuringScreen\turing-smart-screen-python\codex_dino.py

Constantes:
FPS = 3.0
STEP_PX = 6
TRACK_X_MIN = 96
TRACK_X_MAX = 352
TRACK_Y = 277

DESINSTALAR
-----------
python uninstall_dino.py C:\TuringScreen\turing-smart-screen-python

OBSERVACAO
----------
O overlay usa a mesma instancia do display e a mesma fila serial do
turing-smart-screen-python. Ele nao tenta abrir a COM5 separadamente.

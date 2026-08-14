CODEX SYSTEM SHARK ANIMATED
==========================

Conteudo
--------
- Tema completo CodexSystemSharkAnimated
- Tubarao pixel-art animado
- Interacoes:
  1) nada para a direita
  2) para e observa/solta bolhas
  3) nada para a esquerda
  4) abre/fecha a boca
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

   python install_shark.py C:\TuringScreen\turing-smart-screen-python

5. Depois:

   cd C:\TuringScreen\turing-smart-screen-python
   python configure.py

6. Selecione:
   Theme: CodexSystemSharkAnimated
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
- TRACK_Y = 262
- IDLE_SECONDS = 6
- CHOMP_SECONDS = 6
- SLEEP_SECONDS = 18

OBSERVACAO
----------
O instalador ja tenta parar automaticamente a instancia anterior do
turing-smart-screen-python antes de copiar os arquivos e aplicar o patch.

DESINSTALAR
-----------
python uninstall_shark.py C:\TuringScreen\turing-smart-screen-python

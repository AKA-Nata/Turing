CODEX DUCK OVERLAY
==================

Objetivo
--------
Adicionar um pato pixel-art andando da esquerda para a direita e voltando
na faixa livre do rodape do tema CodexSystemPCv3, sem abrir uma segunda
conexao COM e sem substituir o monitor de CPU/GPU/RAM.

Compatibilidade preparada
-------------------------
- turing-smart-screen-python
- Turing Smart Screen 3.5"
- 480x320 landscape
- tema CodexSystemPCv3
- Windows / Python
- usa a mesma fila serial do monitor principal

INSTALACAO
----------
1. Extraia esta pasta em qualquer lugar.

2. Feche o Turing System Monitor caso esteja rodando.

3. Abra PowerShell COMO ADMINISTRADOR.

4. Entre nesta pasta e execute:

   python install_duck.py C:\TuringScreen\turing-smart-screen-python

5. Depois:

   cd C:\TuringScreen\turing-smart-screen-python
   python main.py

O instalador:
- cria main.py.before_codex_duck na primeira instalacao;
- copia codex_duck.py para a raiz do repositorio;
- copia os sprites para res\codex_duck;
- adiciona um pequeno bloco idempotente em main.py.

COMPORTAMENTO PADRAO
--------------------
- 3 FPS
- passo de 6 px
- caminho horizontal x=95 ate x=355
- y=299
- 4 frames para cada direcao
- desacelera automaticamente quando a fila serial esta ocupada

AJUSTES
-------
Abra:
  C:\TuringScreen\turing-smart-screen-python\codex_duck.py

Principais constantes:
  FPS = 3.0
  STEP_PX = 6
  TRACK_X_MIN = 95
  TRACK_X_MAX = 355
  TRACK_Y = 299

Para um pato mais lento:
  FPS = 2.0

Para um movimento mais suave:
  STEP_PX = 4

Para desinstalar:
  python uninstall_duck.py C:\TuringScreen\turing-smart-screen-python

Observacao
----------
O pato e desenhado somente na area vazia entre "PC MONITOR" e "ONLINE".
A regiao anterior e restaurada a partir do background.png do tema antes
de cada novo frame, evitando deixar rastros na tela.

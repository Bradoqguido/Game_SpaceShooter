# 📋 Requirements — Space Shooter

## Visão do Produto

Jogo arcade no estilo Asteroids desenvolvido em Python + Pygame. Todos os gráficos são desenhados proceduralmente pela engine. Comercializado via modelo de assinatura mensal/anual.

---

## User Stories

### US-01 – Controle da Nave
**Como** jogador  
**Eu quero** mover a nave com W A S D  
**Para que** eu possa desviar de asteroides e me posicionar para atirar

**Critérios de Aceite:**
- `W` → aplica thrust na direção atual da nave
- `A` / `D` → rotaciona a nave para esquerda/direita
- `S` → aplica frenagem (brake) suave
- A nave atravessa as bordas da tela (wrap toroidal)
- Partículas de propulsão visíveis ao pressionar `W`

---

### US-02 – Disparo
**Como** jogador  
**Eu quero** atirar com a tecla ESPAÇO  
**Para que** eu possa destruir os asteroides

**Critérios de Aceite:**
- Pressing ESPAÇO dispara um laser na direção da nave
- Som de laser ("pew") reproduzido a cada disparo
- Cooldown de ~0.25s entre disparos
- O laser tem trilha visual brilhante
- O laser desaparece após percorrer distância máxima ou colidir

---

### US-03 – Asteroides
**Como** jogador  
**Eu quero** ver asteroides se movendo pela tela  
**Para que** o jogo ofereça desafio progressivo

**Critérios de Aceite:**
- Asteroides grandes se dividem em 2 médios ao serem atingidos
- Asteroides médios se dividem em 2 pequenos
- Asteroides pequenos são destruídos (explosão de partículas)
- Pontuação: Grande=20pts, Médio=50pts, Pequeno=100pts
- Asteroides atravessam bordas (wrap)

---

### US-04 – Vidas & Game Over
**Como** jogador  
**Eu quero** ter vidas e ver minha pontuação  
**Para que** eu possa acompanhar meu progresso e sentir risco

**Critérios de Aceite:**
- Jogador começa com 3 vidas
- Colisão com asteroide remove 1 vida + invencibilidade temporária
- A 0 vidas → tela de Game Over com opções Reiniciar / Sair
- HUD exibe: pontuação, vidas (ícones), nível atual

---

### US-05 – Menu de Pausa
**Como** jogador  
**Eu quero** pausar o jogo pressionando ESC  
**Para que** eu possa interromper a sessão sem perder progresso

**Critérios de Aceite:**
- ESC → exibe overlay semi-transparente "PAUSADO"
- Opções: "Reiniciar" e "Sair"
- ESC novamente → retorna ao jogo
- O estado do jogo é preservado ao pausar/retomar

---

### US-06 – Progressão de Níveis
**Como** jogador  
**Eu quero** que o jogo fique mais difícil conforme avanço  
**Para que** o desafio se mantenha interessante

**Critérios de Aceite:**
- Ao destruir todos os asteroides → novo nível
- Cada nível adiciona mais asteroides e aumenta velocidade
- Anúncio visual do nível no início de cada onda

---

## Requisitos Não-Funcionais

| # | Requisito |
|---|---|
| NFR-01 | Rodar a ≥ 60 FPS em hardware moderno |
| NFR-02 | Zero dependência de arquivos de imagem ou áudio externos |
| NFR-03 | Compatível com Windows 10+, macOS 12+, Ubuntu 22+ |
| NFR-04 | Instalação via `pip install -r requirements.txt` |
| NFR-05 | Código modular e documentado (docstrings) |

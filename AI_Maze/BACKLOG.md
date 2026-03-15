# 📌 Project Backlog & Future Improvements
*(Para a versão em Português, [clique aqui](#-versão-em-português-brasileiro))*

## 🇺🇸 English Version

### 🎨 Graphics & UI/UX (Next Steps)
- [ ] **Heads-Up Display (HUD):** Create a visual UI overlay displaying real-time metrics:
  - A survival timer that resets every time the Agent crashes.
  - A "High Score" display showing the longest survival streak.
  - A dynamic "Difficulty Level" indicator (based on the current LLM rules: spawn chance and hazard lifetime).
- [ ] **Sprite Integration:** Replace the basic Pygame rectangles with actual 2D sprites (e.g., an indie-style character, textured walls, and animated hazards).
- [ ] **Visual Themes:** Add background colors or tilesets to make it look like a real maze rather than a terminal grid.
- [ ] **XAI Dashboard (Explainable AI):** Display an on-screen log translating the LLM's JSON decisions into natural language reasoning so observers can understand *why* the rules changed.
- [ ] **Explainable AI (XAI) Thought Bubbles:** Implement a UI thought bubble above the agent translating the Q-Table mathematical values into human-readable natural language.

### 🧠 AI & System Architecture
- [ ] **Graceful Degradation (API Fallback):** Implement a "Last Known Good State" memory. If the LLM API drops or times out, the Director should not reset to default difficulty, but instead maintain the last valid rules received until the connection is restored.
- [ ] **Multithreading:** Move the LLM API calls to a background thread to prevent the game loop from pausing/freezing during the network request.
- [ ] **Torus Topology (Pac-Man Effect):** Allow the player to cross the screen borders and appear on the opposite side.
- [ ] **Dynamic Grid Size:** Increase the grid resolution (smaller blocks, larger map) for a more complex maze.

---

## 🇧🇷 Versão em Português Brasileiro

### 🎨 Gráficos & UI/UX (Próximos Passos)
- [ ] **Interface de Bordo (HUD):** Criar uma interface visual sobreposta mostrando métricas em tempo real:
  - Um cronômetro de sobrevivência que reseta sempre que o Agente morre.
  - Um mostrador de "Maior Tempo" (High Score) exibindo o recorde de sobrevivência.
  - Um indicador dinâmico de "Nível de Dificuldade" (baseado nas regras atuais da LLM: taxa de spawn e tempo de vida dos perigos).
- [ ] **Integração de Sprites:** Substituir os retângulos básicos do Pygame por sprites 2D reais (ex: um personagem estilo indie, paredes texturizadas e perigos animados).
- [ ] **Temas Visuais:** Adicionar cores de fundo ou *tilesets* para fazer com que pareça um labirinto real em vez de uma grade de terminal.
- [ ] **Dashboard XAI (IA Explicável):** Mostrar na tela um log traduzindo as decisões em JSON do LLM para raciocínio em linguagem natural, para que observadores entendam *por que* as regras mudaram.
- [ ] **Balões de Pensamento (XAI):** Implementar um balão de pensamento na UI acima do agente traduzindo os valores matemáticos da Q-Table em linguagem natural.

### 🧠 IA & Arquitetura de Sistema
- [ ] **Degradação Graciosa (Fallback da API):** Implementar uma memória de "Último Estado Bom Conhecido". Se a API do LLM cair ou der timeout, o Diretor não deve resetar para a dificuldade padrão, mas sim manter as últimas regras válidas recebidas até que a conexão seja restaurada.
- [ ] **Multithreading:** Mover as chamadas da API do LLM para uma *thread* em segundo plano (background) para evitar que o loop do jogo pause/congele durante a requisição de rede.
- [ ] **Topologia Toroide (Efeito Pac-Man):** Permitir que o jogador atravesse as bordas da tela e apareça no lado oposto.
- [ ] **Tamanho Dinâmico da Grade:** Aumentar a resolução da grade (blocos menores, mapa maior) para um labirinto mais complexo.
# 📌 Project Backlog & Future Improvements
*(Para a versão em Português, [clique aqui](#-versão-em-português-brasileiro))*

## 🇺🇸 English Version

### 🗺️ Level Design & Procedural Generation
- [ ] **Randomized Spawn:** The player should start at a random safe location, not always at (0, 0).
- [ ] **Spawn Protection (Pathfinding):** Implement an algorithm (like A* or Flood Fill) to ensure the player never spawns completely enclosed by hazards. There must always be a valid path/escape.
- [ ] **Torus Topology (Pac-Man Effect):** Allow the player to cross the screen borders and appear on the opposite side.
- [ ] **Dynamic Grid Size:** Increase the grid resolution (smaller blocks, larger map) for a more complex maze.
- [ ] **Graceful Degradation (API Fallback):** Implement a "Last Known Good State" memory. If the LLM API drops or times out, the Director should not reset to default difficulty, but instead maintain the last valid rules received until the connection is restored.

### 🎨 Graphics & Polish
- [ ] **Sprite Integration:** Replace the basic Pygame rectangles with actual 2D sprites (e.g., an indie-style character, textured walls, and animated hazards).
- [ ] **Visual Themes:** Add background colors or tilesets to make it look like a real maze rather than a terminal grid.
- [ ] **Explainable AI (XAI) Thought Bubbles:** Implement a UI thought bubble above the agent. It will translate the Q-Table mathematical values into human-readable natural language (e.g., "Right is dangerous, better go up!"), optionally using LLM generation for deeper reflections during game pauses.
- [ ] **XAI Dashboard (Decision History):** Display an on-screen log showing the agent's decision-making history as Epsilon decays. It should also display the LLM's reasoning for rule changes, bridging mathematical values and natural language for easy understanding.
- [ ] **Heads-Up Display (HUD):** Create a visual UI overlay displaying real-time metrics:
  - A survival timer that resets every time the Agent crashes.
  - A "High Score" display showing the longest survival streak.
  - A dynamic "Difficulty Level" indicator (based on the current LLM rules: spawn chance and hazard lifetime).

### 🧠 AI & Game Logic
- [ ] **Adaptive Epsilon (Epsilon Reset):** Implement a mechanic where the Agent's Epsilon rate slightly increases (e.g., bumps back to 0.3) whenever the LLM Director significantly increases the game's difficulty. This forces the Agent to re-explore and adapt to the new environment rules instead of rigidly following an outdated Q-Table.

---

## 🇧🇷 Versão em Português Brasileiro

### 🗺️ Level Design & Geração Procedural
- [ ] **Spawn Aleatório:** O jogador deve começar em um local seguro e aleatório, e não sempre em (0, 0).
- [ ] **Proteção de Spawn (Pathfinding):** Implementar um algoritmo (como A* ou Flood Fill) para garantir que o jogador nunca nasça completamente cercado por perigos. Deve sempre haver um caminho válido/rota de fuga.
- [ ] **Topologia Toroide (Efeito Pac-Man):** Permitir que o jogador atravesse as bordas da tela e apareça no lado oposto.
- [ ] **Tamanho Dinâmico da Grade:** Aumentar a resolução da grade (blocos menores, mapa maior) para um labirinto mais complexo.
- [ ] **Degradação Graciosa (Fallback da API):** Implementar uma memória de "Último Estado Bom Conhecido". Se a API do LLM cair ou der timeout, o Diretor não deve resetar para a dificuldade padrão, mas sim manter as últimas regras válidas recebidas até que a conexão seja restaurada.

### 🎨 Gráficos & Polimento
- [ ] **Integração de Sprites:** Substituir os retângulos básicos do Pygame por sprites 2D reais (ex: um personagem estilo indie, paredes texturizadas e perigos animados).
- [ ] **Temas Visuais:** Adicionar cores de fundo ou *tilesets* para fazer com que pareça um labirinto real em vez de uma grade de terminal.
- [ ] **Balões de Pensamento (IA Explicável - XAI):** Implementar um balão de pensamento na UI acima do agente. Ele traduzirá os valores matemáticos da Q-Table em linguagem natural humana (ex: "A direita é perigosa, melhor ir para cima!"), usando opcionalmente geração via LLM para reflexões mais profundas durante pausas do jogo.
- [ ] **Dashboard XAI (Histórico de Decisões):** Mostrar na tela um log com o histórico de decisões do agente enquanto o Epsilon decai. Deve exibir também o raciocínio do LLM para as mudanças de regras, unindo os valores matemáticos e a linguagem natural para fácil entendimento.
- [ ] **Interface de Bordo (HUD):** Criar uma interface visual sobreposta mostrando métricas em tempo real:
  - Um cronômetro de sobrevivência que reseta sempre que o Agente morre.
  - Um mostrador de "Maior Tempo" (High Score) exibindo o recorde de sobrevivência.
  - Um indicador dinâmico de "Nível de Dificuldade" (baseado nas regras atuais da LLM: taxa de spawn e tempo de vida dos perigos).

### 🧠 IA & Lógica do Jogo
- [ ] **Epsilon Adaptativo (Reset de Epsilon):** Implementar uma mecânica onde a taxa de Epsilon do Agente sobe levemente (ex: volta para 0.3) sempre que o Diretor LLM aumentar significativamente a dificuldade do jogo. Isso força o Agente a re-explorar e se adaptar às novas regras do ambiente em vez de seguir rigidamente uma Q-Table desatualizada.
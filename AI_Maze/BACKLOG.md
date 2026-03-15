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
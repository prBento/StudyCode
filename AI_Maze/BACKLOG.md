# 📌 Project Backlog & Future Improvements
*(Para a versão em Português, [clique aqui](#-versão-em-português-brasileiro))*

## 🇺🇸 English Version

### 🎨 Graphics & UI/UX
- [x] **Heads-Up Display (HUD):** Create a visual UI overlay displaying real-time metrics (Survival timer, High Score, Difficulty Level).
- [x] **Sprite Integration:** Replace basic rectangles with dynamic geometric sprites (animated robots and pulsating hazards).
- [x] **Visual Themes:** Add cybernetic grid background for spatial awareness.
- [x] **XAI Dashboard (Director):** Display an on-screen log translating the LLM's JSON decisions into natural language.
- [x] **Agent XAI Panel:** Implement a UI panel translating the Q-Table mathematical values and radar into human-readable natural language.
- [x] **Visual Hitbox Correction:** Sync visual lerp position with crash coordinates for accurate explosion feedback.
- [ ] **Ultra-Fluid Movement (Time-based Lerp):** Upgrade the current lerp to be completely time-dependent, eliminating any remaining "tic-tac" stopping effect between blocks.
- [ ] **Graphic Overhaul:** Refine the design of the agent and environment to look like a modern Sci-Fi UI/UX rather than basic geometric shapes.

### 🧠 AI & System Architecture
- [x] **Multithreading:** Move the LLM API calls to a background thread to prevent game freezing.
- [ ] **Initial Learning Curve (Onboarding):** Start the first epoch with very low hazards so the AI can safely explore and populate its Q-Table before the Director steps in.
- [ ] **Graceful Degradation (API Fallback):** Implement a "Last Known Good State" memory if the LLM API drops or times out.
- [ ] **Torus Topology (Pac-Man Effect):** Allow the player to cross screen borders.
- [ ] **Dynamic Grid Size:** Increase grid resolution for a more complex maze.

---

## 🇧🇷 Versão em Português Brasileiro

### 🎨 Gráficos & UI/UX
- [x] **Interface de Bordo (HUD):** Criar uma interface visual com métricas em tempo real (Cronômetro, Recorde, Dificuldade).
- [x] **Integração de Sprites:** Substituir retângulos básicos por sprites geométricos dinâmicos (robô animado e minas pulsantes).
- [x] **Temas Visuais:** Adicionar grade cibernética no fundo para noção espacial.
- [x] **Dashboard XAI (Diretor):** Mostrar log traduzindo as decisões do LLM para linguagem natural.
- [x] **Painel XAI do Agente:** Implementar painel traduzindo valores da Q-Table e radar para linguagem natural.
- [x] **Correção de Hitbox Visual:** Sincronizar posição visual com coordenadas reais na hora da explosão.
- [ ] **Movimentação Ultra-Fluida (Lerp por Tempo):** Melhorar a interpolação linear para ser totalmente dependente do tempo, eliminando qualquer "paradinha" (tic-tac) entre os blocos.
- [ ] **Overhaul Gráfico:** Refinar o design para sair de formas básicas e ir para um visual Sci-Fi mais comercial e moderno.

### 🧠 IA & Arquitetura de Sistema
- [x] **Multithreading:** Mover requisições do LLM para segundo plano para evitar travamentos.
- [ ] **Curva de Aprendizado Inicial (Onboarding):** Iniciar a primeira rodada com perigos quase zerados para a IA explorar com segurança antes do Diretor agir.
- [ ] **Degradação Graciosa (Fallback da API):** Manter últimas regras válidas se a conexão com o LLM cair.
- [ ] **Topologia Toroide (Efeito Pac-Man):** Permitir atravessar as bordas da tela.
- [ ] **Tamanho Dinâmico da Grade:** Aumentar resolução para labirintos mais complexos.
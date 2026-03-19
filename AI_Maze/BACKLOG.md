# 📌 Project Backlog & Future Improvements
*(Para a versão em Português, [clique aqui](#-versão-em-português-brasileiro))*

## 🇺🇸 English Version

### 🎨 Graphics & UI/UX
- [x] **Heads-Up Display (HUD):** Create a visual UI overlay displaying real-time metrics.
- [x] **Sprite Integration:** Replace basic rectangles with dynamic geometric sprites.
- [x] **Visual Themes:** Add cybernetic grid background for spatial awareness.
- [x] **XAI Dashboard (Director):** Display an on-screen log translating the LLM's decisions.
- [x] **Visual Hitbox Correction:** Sync visual lerp position with crash coordinates.
- [x] **Ultra-Fluid Movement:** Upgrade lerp to be completely time-dependent (Time-based Lerp).
- [x] **Agent XAI Panel:** Implement a UI panel translating the Q-Table mathematical values and radar into human-readable natural language.
- [ ] **Graphic Overhaul:** Refine the design of the agent and environment to look like a modern Sci-Fi UI/UX.

### 🧠 AI & System Architecture
- [x] **Multithreading:** Move the LLM API calls to a background thread.
- [x] **Initial Learning Curve (Onboarding):** Start the first epoch with very low hazards.
- [x] **Diagonal Movement:** Expand AI action space to 8 directions.
- [x] **Advanced Collision Physics:** Prevent diagonal corner-cutting ghosting by adding intermediate hazard checks.
- [x] **Torus Topology (Pac-Man Effect):** Allow the player to cross screen borders.
- [ ] **Graceful Degradation (API Fallback):** Implement a "Last Known Good State" memory if the LLM API drops.

---

## 🇧🇷 Versão em Português Brasileiro

### 🎨 Gráficos & UI/UX
- [x] **Interface de Bordo (HUD):** Criar uma interface visual com métricas em tempo real.
- [x] **Integração de Sprites:** Substituir retângulos básicos por sprites geométricos dinâmicos.
- [x] **Temas Visuais:** Adicionar grade cibernética no fundo.
- [x] **Dashboard XAI (Diretor):** Mostrar log traduzindo as decisões do LLM.
- [x] **Correção de Hitbox Visual:** Sincronizar posição visual com coordenadas reais na explosão.
- [x] **Movimentação Ultra-Fluida:** Interpolação linear dependente do tempo para movimento contínuo.
- [x] **Painel XAI do Agente:** Implementar painel traduzindo valores da Q-Table e radar para linguagem natural.
- [ ] **Overhaul Gráfico:** Refinar o design para um visual Sci-Fi mais comercial e moderno.

### 🧠 IA & Arquitetura de Sistema
- [x] **Multithreading:** Mover requisições do LLM para segundo plano.
- [x] **Curva de Aprendizado (Onboarding):** Iniciar a primeira rodada com perigos quase zerados.
- [x] **Movimentação Diagonal:** Expandir as ações da IA para 8 direções.
- [x] **Física de Colisão Avançada:** Impedir ghosting diagonal adicionando checagem de impacto nas quinas.
- [x] **Topologia Toroide (Efeito Pac-Man):** Permitir atravessar as bordas da tela.
- [ ] **Degradação Graciosa (Fallback da API):** Manter últimas regras válidas se a conexão com o LLM cair.
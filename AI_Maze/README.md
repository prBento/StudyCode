# 🧠 Hybrid AI Maze: Q-Learning Agent vs LLM Game Director
*(Para a versão em Português, [clique aqui](#-versão-em-português-brasileiro))*

## 🇺🇸 English Version

### 🎯 About the Project
This is a study project focused on Artificial Intelligence and Game Development. The goal is to create a dynamic environment where an Agent (the player character) learns to survive using local **Reinforcement Learning (Q-Learning)**, while the game environment is controlled by an **LLM-based Game Director**. The LLM analyzes the agent's performance and adjusts the maze's difficulty, topology, and hazard spawn rates in real-time.

🤖 **AI Assistance Note:** This project is being developed with the educational support and assistance of Google's **Gemini AI**, acting as a pair programmer and technical mentor.

### 🛠️ Tech Stack
* **Language:** Python
* **Graphics Engine:** Pygame
* **Agent AI:** Q-Learning (Local Reinforcement Learning)
* **Environment AI:** LLM API Integration (Gemini)

### 🧠 AI Architecture: Why Q-Learning?
For the Agent's brain, we chose **Tabular Q-Learning** over more complex Deep Learning models (like DQN) for the following reasons:
1. **Discrete State Space:** The grid-based nature of our maze makes it perfect for a finite state representation. The agent can map its immediate surroundings (e.g., walls adjacent to it) as clear, discrete states.
2. **Transparency:** Unlike Neural Networks (which act as "black boxes"), a Q-Table is entirely transparent. We can pause the game and read exactly *why* the agent chose a specific action by looking at the mathematical values assigned to each state.
3. **The Bellman Equation:** The agent updates its knowledge using the Bellman Equation. This is crucial because it allows the AI to value *future, long-term rewards* (surviving) rather than just making greedy, immediate choices. Through the Discount Factor ($\gamma$), the agent learns to avoid paths that look safe now but lead to dead-ends later.

### 🚦 Git & Commit Standards
To maintain a clean and professional history, this project follows the *Conventional Commits* specification:
* `feat:` For new features
* `fix:` For bug fixes
* `docs:` For documentation updates
* `refactor:` For code improvements that do not change behavior

**Branching Strategy:**
* `main`: Stable and functional code.
* `feature/feature-name`: For developing new features before merging into main.

### 🗺️ Development Roadmap
- [x] 1. Foundation: Pygame setup, window creation, and basic grid movement.
- [x] 2. Base Mechanics: Static collisions, walls, and fixed hazards (Game Over logic).
- [x] 3. Procedural Generation: Dynamic maze generation algorithm.
- [ ] 4. The Muscle (Agent): Implementation of the Q-Learning algorithm.
- [ ] 5. Dynamic Hazards: Time-based obstacles (teaching the agent to "wait").
- [ ] 6. The Brain (Director): LLM integration to adjust difficulty based on agent performance.

### 🔮 Future Backlog
Check out our [`BACKLOG.md`](BACKLOG.md) file for a list of planned features, including graphics overhaul, pathfinding spawn protection, and torus topology.

---

## 🇧🇷 Versão em Português Brasileiro

### 🎯 Sobre o Projeto
Este é um projeto de estudo focado em Inteligência Artificial e Desenvolvimento de Jogos. O objetivo é criar um ambiente dinâmico onde um Agente (o personagem) aprende a sobreviver usando **Aprendizado por Reforço (Q-Learning)** localmente, enquanto o ambiente do jogo é controlado por um **Game Director baseado em LLM**. O LLM analisa o desempenho do agente e ajusta a dificuldade, a topologia do labirinto e a taxa de surgimento de perigos em tempo real.

🤖 **Nota de Assistência de IA:** Este projeto está sendo desenvolvido com o apoio educacional e assistência da IA **Gemini** do Google, atuando como um *pair programmer* (programador em par) e mentor técnico.

### 🛠️ Stack Tecnológico
* **Linguagem:** Python
* **Motor Gráfico:** Pygame
* **IA do Agente:** Q-Learning (Aprendizado por Reforço Local)
* **IA do Ambiente:** Integração via API com LLM (Gemini)

### 🧠 Arquitetura da IA: Por que Q-Learning?
Para o cérebro do Agente, escolhemos o **Q-Learning Tabular** em vez de modelos mais complexos de Deep Learning (como DQN) pelos seguintes motivos:
1. **Espaço de Estados Discreto:** A natureza em grade (grid) do nosso labirinto o torna perfeito para uma representação de estados finita. O agente consegue mapear seus arredores imediatos como estados claros e discretos.
2. **Transparência:** Diferente de Redes Neurais (que funcionam como "caixas pretas"), uma Tabela-Q é totalmente transparente. Podemos pausar o jogo e ler exatamente *por que* o agente tomou uma ação específica apenas olhando os valores matemáticos de cada estado.
3. **A Equação de Bellman:** O agente atualiza seu conhecimento usando a Equação de Bellman. Isso é vital porque permite que a IA valorize *recompensas futuras de longo prazo* (sobrevivência) em vez de focar apenas no momento imediato. Através do Fator de Desconto ($\gamma$), o agente aprende a evitar caminhos que parecem seguros agora, mas que levam a becos sem saída mais tarde.

### 🚦 Padrões de Git e Commits
Para manter um histórico limpo e profissional, este projeto segue a especificação *Conventional Commits*:
* `feat:` Para novas funcionalidades
* `fix:` Para correção de bugs
* `docs:` Para atualizações de documentação
* `refactor:` Para melhorias de código que não alteram o comportamento

**Estratégia de Branches:**
* `main`: Código estável e funcional.
* `feature/nome-da-feature`: Para o desenvolvimento de novas funcionalidades antes de mesclar com a `main`.

### 🗺️ Roadmap de Desenvolvimento
- [x] 1. Fundação: Configuração do Pygame, criação da janela e movimento básico em grade.
- [x] 2. Mecânica Base: Colisões estáticas, paredes e perigos fixos (Lógica de Game Over).
- [x] 3. Geração Procedural: Algoritmo dinâmico de geração de labirinto.
- [ ] 4. O Músculo (Agente): Implementação do algoritmo Q-Learning.
- [ ] 5. Perigos Dinâmicos: Obstáculos baseados em tempo (ensinando o agente a "esperar").
- [ ] 6. O Cérebro (Diretor): Integração com LLM para ajustar a dificuldade com base no desempenho do agente.

### 🔮 Backlog Futuro
Confira nosso arquivo [`BACKLOG.md`](BACKLOG.md) para ver a lista de funcionalidades planejadas, incluindo melhoria de gráficos, proteção de spawn com *pathfinding* e topologia toroide.
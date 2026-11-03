# Epidemics and Social Contagion Agent-based Simulator (ESCAS)

## About

**ESCAS** is an agent-based epidemic simulator developed as a first-year Master's (M1 IMPAIRS) project at Université Paris Cité. Built entirely from scratch in Python, utilizing an object-oriented architecture, custom state machines, and an interactive graphical interface powered by `pygame` and `pygame_gui`. 

The simulation features a dynamic environment where independent agents move with individual behavioral traits—such as normal routines, panic, or confinement—interacting in real-time with a compartmental epidemiological model (SIR) to analyze the spread of pathogens.

*Note: Due to tight time constraints during development, certain advanced behavioral interactions and fine-tuned mechanics are implemented in a basic or experimental state. The codebase might contains some and user interface are primarily in French.*

## Tech Stack

- **Language:** Python 3.x
- **GUI & Visualization:** `pygame`, `pygame_gui`, `matplotlib`
- **Architecture:** Agent-Based Modeling (ABM), Compartmental epidemiological modeling (SIR)

## Key Features

- **Agent-Based Simulation:** Independent agents moving within a 2D environment with individual states (Susceptible/Sain, Infected/Infecté, Recovered/Guéri) and behavioral attitudes (Normal, Panic, Confined).
- **Epidemiological Engine:** Pathogen management featuring adjustable contagion radius, transmission probability, and healing ticks.
- **Interactive GUI:** Built with Pygame and `pygame_gui`, offering real-time controls, adjustable parameters via sliders, and agent inspection.
- **Import & Export Configuration:** Ability to save and load simulation parameters seamlessly via JSON configuration files.
- **Data Export & Analysis:** Support for exporting simulation snapshots to JSON and generating live population evolution graphs.

## Known Limitations & Constraints

Due to limited development time, certain features come with minor compromises:
- **Behavioral Complexity:** Social contagion and psychological states (like panicking crowds or widespread confinement) operate on simplified heuristics rather than complex multi-agent feedback loops.
- **Edge Cases:** Graphical rendering or real-time slider scaling during heavy simulations can occasionally show minor performance hiccups.

## Project Structure

```text
📁 fsh/
│
├── 📁 docs/
│   └── 📄 soutenance_chiv_chen.pdf     # Project defense slides
│
├── 📁 src/
│   └── 📁 main/
│       ├── 📁 res/
│       │   ├── 📁 input/               # Simulation configuration profiles (JSON)
│       │   └── 📁 theme/               # UI theme and styling assets
│       ├── agent.py                    # Agent behaviors, movement, and states
│       ├── agentFactory.py             # Agent creation helpers
│       ├── environnement.py            # 2D environment boundaries and layout
│       ├── etat.py                     # Health and attitude enums
│       ├── main.py                     # Application entry point & configuration
│       ├── pathogene.py                # Pathogen configuration (radius, probability)
│       ├── simulation.py               # Core simulation loop and SIR tracking
│       ├── utils.py                    # Utility functions (clamping, random choices)
│       └── view.py                     # Pygame graphical interface and UI panels
│
├── 📄 LICENSE                          # License of the project
└── 📄 README.md                        # Project documentation
```

## Getting Started

### Prerequisites

* Python 3.x.

### Installation & Execution

1. Clone the repository:
```bash
git clone https://github.com/SuyuKuka/escas-agent-based-epidemic-simulator.git escas
cd escas
```

2. Install dependencies:
```bash
pip install pygame pygame_gui matplotlib
```

3. Run the simulation:
```bash
python src/main/main.py
```

### Configuration Import & Export

The application supports loading and saving simulation configurations via JSON files located in `src/main/res/input/`:
- **Export:** When clicking the **Export** button in the GUI, your current configuration is saved to `src/main/res/input/config.json`.
- **Import:** The application loads its settings directly from `src/main/res/input/config.json`.

#### Preset Simulations

We have included two preset simulation profiles trying to reproduce specific outbreaks:
- `covid.json` (COVID-19 strain)
- `hantavirus.json` (Hantavirus strain)

To test one of these presets, simply rename your chosen file (e.g., `covid.json`) to **`config.json`** inside the `src/main/res/input/` directory and then click on the import button.

## Team

This project was developed collaboratively as 2-person team:

- **CHEN Michel** - Simulation Logic & Architecture
  [![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?logo=github)](https://github.com/SuyuKuka)
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?logo=linkedin)](https://linkedin.com/in/chen-michel)

- **CHIV Henri** - Simulation Logic & Architecture
  [![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?logo=github)](https://github.com/H-flamme)

## License

This project is licensed under the GPL 3.0 License — see [LICENSE](LICENSE) for details.
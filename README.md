#  Bacterial Evolution: Artificial Life Sandbox

An artificial life simulation built with **Python** and **Pygame**.
Watch as digital bacteria evolve, hunt, flee, and reproduce in a competitive ecosystem. The simulation uses natural selection principles: only the fittest survive to pass on their DNA.

![Simulation Demo](bacteria.gif)

##  Key Features

###  Complex Behavior (AI)
* **Blue Bacteria (Prey):** Herbivores that wander in search of food. They possess a **Fear System**, allowing them to detect predators and flee in the opposite direction to survive.
* **Red Bacteria (Predator):** Carnivores that hunt Blue bacteria. They utilize energy-conservation tactics (ambushing) and must eat to survive.
* **Violet Bacteria (Omnivore):** (*Configurable*) adaptable entities that can eat both plants and other bacteria based on availability.

### Genetics & Evolution
Every bacterium has a unique **DNA** genome that determines its traits:
* **Speed:** How fast it moves (costs more energy).
* **Sense Radius:** How far it can "see" food or danger.
* **Fear Radius:** At what distance it starts running from predators.
* **Reproduction Rate:** The probability of offspring.

When bacteria reproduce, their DNA is passed down with slight **mutations**. Over time, you will see the population evolve strategies (e.g., becoming faster or "smarter").

### Technical Optimization
The project implements a **Spatial Partitioning Grid**. instead of checking every object against every other object ($O(N^2)$), entities only check their local grid cells. This allows the simulation to handle hundreds/thousands of agents with high FPS.

---

##  Controls

| Key | Action |
| :--- | :--- |
| **SPACE** | Pause / Resume simulation |
| **UP Arrow** | Increase simulation speed (Target FPS) |
| **DOWN Arrow** | Decrease simulation speed |
| **Mouse** | Resize the window (UI adapts automatically) |

##  Configuration

You can tweak the laws of physics and biology in `settings.py`:
* **`WORLD_SIZE`**: Change the map dimensions.
* **`MITOSIS_RATE`**: How often bacteria try to reproduce.
* **`PENALTY_...`**: Adjust the metabolic cost of movement and health.
* **`MAX_AGE`**: Set lifespans to force generational turnover.

##  Live Stats
The simulation includes a real-time graph at the bottom of the screen tracking:
* **Green Line:** Amount of Food.
* **Blue Line:** Population of Prey.
* **Red Line:** Population of Predators.

---
*Created with Python 3 and Pygame.*

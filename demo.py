import lifeos

# --- GENOME ---
print("=== GENOME DEMO ===")
genome = lifeos.genome.Genome(length=12)
print("Initial Genome:", genome)

# Mutate the genome
genome.mutate(rate=0.2)
print("After Mutation:", genome)


# --- LINEAGE ---
print("\n=== LINEAGE DEMO ===")
tracker = lifeos.lineage.LineageTracker()
tracker.add_individual("Adam", genome)
print("Lineage records:", tracker.history)


# --- REPRODUCTION ---
print("\n=== REPRODUCTION DEMO ===")
parent1 = lifeos.genome.Genome(length=12)
parent2 = lifeos.genome.Genome(length=12)

child = lifeos.reproduction.reproduce(parent1, parent2)
print("Parent 1:", parent1)
print("Parent 2:", parent2)
print("Child   :", child)


# --- MULTIVERSE ---
print("\n=== MULTIVERSE DEMO ===")
universe = lifeos.multiverse.Multiverse()

# Add some individuals
for i in range(3):
    g = lifeos.genome.Genome(length=8)
    universe.add_individual(f"Being_{i}", g)

# Run a simple step in the universe
universe.evolve(steps=2)

# Show population
print("Universe population:", list(universe.population.keys()))

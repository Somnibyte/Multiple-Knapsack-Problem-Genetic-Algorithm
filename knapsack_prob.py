# Author: Guled
# Problem: Multiple Knapsack
from genetic_toolkit import Population,Chromosome,BiologicalProcessManager
import statistics
import random

'''
	Generation Evaluation Function
'''
def find_the_best(population):
	best = None
	for individual in population:
		if best == None or individual.fitness > best.fitness:
			best = individual
	return best.fitness

# Global Variables
crossover_rate = 0.70

# Initialize population with random candidate solutions
population = Population(500)
population.initialize_population()
# Set the mutation rate
mutation_rate = 1/population.populationSize
# Get a reference to the number of knapsacks
numberOfKnapsacks = population.numberOfKnapsacks


generation_counter = 0
while(generation_counter != 100):
	current_population_fitnesses = [chromosome.fitness for chromosome in population.population]
	print("CURRENT GEN FITNESS: {} \n ".format(current_population_fitnesses))
	new_gen = []
	while(len(new_gen) != population.populationSize):
		# Create tournament for tournament selection process
		tournament = [population.population[random.randint(1, population.populationSize-1)] for individual in range(1, population.populationSize)]
		# Obtain two parents from the process of tournament selection
		parent_one, parent_two = population.select_parents(tournament)
		# Create the offspring from those two parents
		child_one,child_two = BiologicalProcessManager.crossover(crossover_rate,parent_one,parent_two)

		# Try to mutate the children
		BiologicalProcessManager.mutate(mutation_rate, child_one, numberOfKnapsacks)
		BiologicalProcessManager.mutate(mutation_rate, child_two, numberOfKnapsacks)

		# Evaluate each of the children
		child_one.generateFitness(population.knapsackList)
		child_two.generateFitness(population.knapsackList)

		# Add the children to the new generation of chromsomes
		new_gen.append(child_one)
		new_gen.append(child_two)

	# Replace old generation with the new one
	population.population = new_gen
	generation_counter += 1

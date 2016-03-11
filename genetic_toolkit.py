import random
import linecache
import copy
from collections import namedtuple

# Class to represent biological processes
class BiologicalProcessManager:
		'''
			Crossover Function

			- The process of One-Point crossover is exercised in this function.
		'''
		def crossover(crossover_rate, parentOne, parentTwo):
			random_probability = random.random()

			if random_probability < crossover_rate:
				return (parentOne, parentTwo)
			else:
				pivot = random.randint(0, len(parentOne.genotype_representation)-1)

				child_one_genotype = parentOne.genotype_representation[:pivot] + parentTwo.genotype_representation[pivot:]
				child_two_genotype = parentTwo.genotype_representation[:pivot] + parentOne.genotype_representation[pivot:]

				child_one = Chromosome(parentOne.numberOfKnapsacksReference, parentOne.numberOfObjectsReference, child_one_genotype)
				child_two = Chromosome(parentOne.numberOfKnapsacksReference, parentOne.numberOfObjectsReference, child_two_genotype)

				child_one.phenotype_representation = parentOne.phenotype_representation
				child_two.phenotype_representation = parentOne.phenotype_representation


				return (child_one, child_two)

		'''
			Mutation function

			- The process of Random Resetting is exercised in this function.
		'''
		def mutate(mutation_rate, child, numberOfKnapsacks):
			for index, position in enumerate(child.genotype_representation):
				random_probability = random.random()
				'''
					(Random Resetting) "Flip" the position with another knapsack if probability < mutation_rate
				'''
				if random_probability < mutation_rate:
					child.genotype_representation[index] = random.randint(0,numberOfKnapsacks)

# Class to represent chromosome
class Chromosome:

	fitness = None # Chromosomes fitness
	phenotype_representation = None # Phenotype representation

	def __init__(self, numOfKnapsacks, numOfObjects, genotype_representation = None):
		self.numberOfKnapsacksReference = numOfKnapsacks
		self.numberOfObjectsReference = numOfObjects

		if genotype_representation == None:
			self.genotype_representation = [random.randint(0,(numOfKnapsacks)) for x in range(0, numOfObjects)]
		else:
			self.genotype_representation = genotype_representation

		self.length_of_encoding = len(self.genotype_representation)

	'''
	 Generates a fitness for all the chromosomes by aggregating their benefits/values
	'''
	def generateFitness(self, knapsackList):
		''' Make a copy of the knapsack list to be used to evaluate if objects in the chromsome
			exceed C using the 'amountUsed' attribute
		'''
		#print("ORIGINAL CHROM: {}".format(self.genotype_representation))
		knapsacks = copy.deepcopy(knapsackList)
		fitnessScore = 0
		done = False
		for i, placement_of_object in enumerate(self.genotype_representation):
			if placement_of_object == 0:
				continue
			else:
				for knapsack in knapsacks:
					if knapsack.id == placement_of_object:
						# if it's over the capacity, change it's bag and revaluate
						if self.phenotype_representation[i].weight > knapsack.capacity:
							while(not done):

								self.genotype_representation[i] = random.randint(0,(self.numberOfKnapsacksReference))

								if self.genotype_representation[i] == 0:
									break
								else:
									current_knapsack = next((sack for sack in knapsacks if sack.id == self.genotype_representation[i]),None)
									if self.phenotype_representation[i].weight > current_knapsack.capacity:
										continue
									if self.phenotype_representation[i].weight <= current_knapsack.capacity:
										fitnessScore += self.phenotype_representation[i].value
										'''We now subtract the objects weight by the knapsacks capacity
										   so that we can keep track of how much space the knapsack has left
										   in the event that another object goes into the same knapsack
										'''
										current_knapsack.capacity = (current_knapsack.capacity - self.phenotype_representation[i].weight)
										break
						else:
							fitnessScore += self.phenotype_representation[i].value
							'''We now subtract the objects weight by the knapsacks capacity
							   so that we can keep track of how much space the knapsack has left
							   in the event that another object goes into the same knapsack
							'''
							knapsack.capacity = (knapsack.capacity - self.phenotype_representation[i].weight)


		# update the chromosomes fitness
		self.fitness = fitnessScore




class Knapsack:
	def __init__(self, id, capacity):
		self.id = id
		self.capacity = capacity

class Population:

	Phenotype = namedtuple('Phenotype', 'id weight value')
	knapsackList = [] # list of knapsacks
	knapSackEvaluationList = [] # used for generating fitness of chromosomes
	population = []

	def __init__(self, size):
		self.populationSize = size
		self.numberOfKnapsacks = 0

	def select_parents(self,tournament):
		'''
			Tournament selection is being used to find two parents
		'''
		first_fittest_indiv = None
		second_fittest_indiv = None

		for individual in tournament:
			# Check if this indivudal is fitter than the current fittist individual
			if first_fittest_indiv == None or individual.fitness > first_fittest_indiv.fitness:
				first_fittest_indiv = individual

		tournament.remove(first_fittest_indiv)

		for individual in tournament:
			# Check if this indivudal is fitter than the current fittist individual
			if second_fittest_indiv == None or individual.fitness > second_fittest_indiv.fitness:
				second_fittest_indiv = individual

		#print("FIRST: {},  SECOND: {}".format(first_fittest_indiv.fitness,second_fittest_indiv.fitness))
		return (first_fittest_indiv,second_fittest_indiv)


	def initialize_population(self):
		'''
			Read from a file and create the chromosomes
		'''
		# Open data file
		dataFile = open('data.txt','r')

		# Read how many knapsacks there will be. (We read the first byte)
		numOfKnapsacks = int(dataFile.read(1))
		self.numberOfKnapsacks = numOfKnapsacks
		#print("NUMBER OF KNAPSACKS: {} \n".format(numOfKnapsacks))
		dataFile.seek(0,0);

		# Read how many objects there will be.
		numOfObjects = int(dataFile.readlines()[numOfKnapsacks+1])

		# Create knapsack dictionary
		lines_to_read = []
		for num in range(0, numOfKnapsacks):
			lines_to_read.append(num)

		dataFile.seek(0,0)
		for i,line in enumerate(dataFile):
			if i == 0:
				continue
			elif i > 0 and i < numOfKnapsacks + 1:
				capacity = int(line)
				self.knapsackList.append(Knapsack((i), capacity))

		# Create phenotype representation of chromosome
		phenotype_representation = []
		lineNumberOffset = numOfKnapsacks + 3 # file offset used to find the objects in the file
		for i in range(0,numOfObjects):
			value,weight = linecache.getline("data.txt", lineNumberOffset+i).split()
			# Create the phenotype representation for each chromsome
			phenotype_representation.append(self.Phenotype(i, int(value),int(weight)))

		# Create the initial population
		for j in range(0,self.populationSize):
			# Create a new chromosome
			new_chromosome = Chromosome(numOfKnapsacks,numOfObjects)
			#  Give each chromosome it's phenotype representation
			new_chromosome.phenotype_representation = phenotype_representation
			# Evaluate each chromosome
			new_chromosome.generateFitness(self.knapsackList)
			# Add the chromsome to the population
			self.population.append(new_chromosome)

		dataFile.close()

'''
A simple evolution simulator that uses a list of individuals, each with a single inheritable power level.
Every generation, individuals with a power level below the environmental pressure have a chance to die
proportional to their lacking power squared. New creatures are then spawned (up to two times the number of
surviving creatures), inheriting the power level of the survivors with a random offset applied.
'''

import random as R

'''
Function definitions.
'''

# Initialize the list with the provided number of individuals, with a symmetrical triangular distribution of power levels between 0 and 5.
def initialize(pop):
    p = []
    n = 0

    for i in range(0, pop):
        v = {'s': R.triangular(0, 5),
             'l': 'Alive',
             'id': n,
             'a': 0}
        p.append(v)
        n += 1
        
    return (p, n)

# Calculates and returns the average power of each alive individual in the population.
def parent_power(p, pop):
    sum = 0
    count = 0
    
    for i in range(0, pop):
        if p[i]['l'] == 'Alive':
            sum += p[i]['s']
            count += 1
    
    if count == 0:
        return 0, 0
    return sum / count, count

# Given a fitness value, determines whether it should result in death.
def kill(f):
    # Check that the individual is less fit than the environment demands
    if f > 0:
        # Repeat a 40% chance of death for every point of missing fitness squared
        for i in range(0, int(f) ** 2):
            if R.random() > 0.6:
                return True
        return False

# Compares the environmental pressure to the power of each living individual to see who will be killed.
def pressure(p, gen, pop):
    pressure = (gen + 5) * (0.8 + (gen / 200))
    
    for i in range(0, pop):
        fitness = pressure - p[i]['s']
        # Change the life status of every creature who should be killed
        if kill(fitness):
            p[i]['l'] = 'Dead'
            
    return p, pressure

# For populations under 20 creatures, prints every individual's id and power. Calculates and returns the strongest, weakest and oldest living individuals.
def print_living(p, pop):
    weak = 0
    wid = 0
    strong = 0
    sid = 0
    old = 1
    oid = 0
    
    for i in p:
        if i['l'] == "Alive":
            # Print every creature for small initial population sizes
            if pop <= 20:
                print('Creature %d: %42f' % (i['id'], i['s']))
            if weak > i['s'] or weak == 0:
                weak = i['s']
                wid = i['id']
            if strong < i['s']:
                strong = i['s']
                sid = i['id']
            if old < i['a']:
                old = i['a']
                oid = i['id']
    
    # Only print the special creature information for large populations
    if pop > 20:
        print('The weakest survivor is Creature %d, which has only %4.2f power. The strongest is Creature %d, at %4.2f power!' % (wid, weak, sid, strong))
        if old > 1:
            print('The oldest creature is number %d, surviving for %d generations.' % (oid, old))
            
    return strong, sid, old, oid

# Prints the stats of the oldest and most fit individuals at the end of the simulation.
def print_stats(gen, n, fittest, fitid, old_env, oldest, oldid, oldgen):
    print('\n### Stats ###')
    print('The population survived %d generations, over which time %d individuals were born. The oldest creature to ever live, Creature %d, experienced %d generations from #%d to #%d.' % (gen + 1, n + 1, oldid, oldest, oldgen - oldest, oldgen))
    print('The most fit individual of all time was Creature %d, who had %4.2f more power than the enviromental pressure at the time, %4.2f.' % (fitid, fittest, old_env))

# Runs the evolution simulation with the provided initial population size (also the maximum) and maximum number of generations.
def simulate(pop, generations):
    p, n = initialize(pop)
    # Overall stats to display at the end of the simulation
    fittest = 0
    fitid = 0
    old_env = 0
    oldest = 0
    oldid = 0
    oldgen = 0
    
    # Loop until the requested number of generations pass, or the population dies out
    for gen in range(0, generations):
        print('\n### Generation %d ###' % gen)
        avg, count = parent_power(p, pop) # calculate the average power of the living individuals for populating the next generation
        # End the simulation if every creature has died
        if avg == 0 or count == 1:
            print("Population went extinct.")
            print_stats(gen, n, fittest, fitid, old_env, oldest, oldid, oldgen)
            return
        else:
            print('%d individuals survived.' % count)
        # Print an analysis of the survivors
        strong, sid, old, oid = print_living(p, pop)
        
        # Increase the mutation chance over time, and as the population gets smaller
        mut = (gen / 100) + 3 + (6 / count) ** 2
        new = count * 2
        
        # Respawn the dead individuals with power randomly offset from the average of the surviving creatures
        for i in range(0, pop):
            # Make sure no more children than two times the number of survivors are spawned
            if new == 0:
                break
            if p[i]['l'] == 'Dead':
                p[i] = {'s': avg + R.uniform(-1 * mut, mut),
                        'l': 'Alive',
                        'id': n,
                        'a': 0}
                n += 1
                new -= 1
            else:
                p[i]['a'] += 1
                
        print('%d new children will be born this generation, with a mutation chance of %4.2f.' % ((count * 2) - new, mut))
                
        # Compare the environmental pressure with each individual's power to see who will die
        p, env = pressure(p, gen, pop)
        print('Average power: %4.2f. Current environmental pressure: %4.2f\n' % (avg, env))
        
        # Compare the oldest and most fit individuals from this generation to the historic highest values
        if strong - env > fittest:
            fittest = strong - env
            fitid = sid
            old_env = env
        if old > oldest:
            oldest = old
            oldid = oid
            oldgen = gen

    print('Population succeeded!')
    print_stats(gen, n, fittest, fitid, old_env, oldest, oldid, oldgen)
    return

'''
Script main.
'''

try:
    maxpop = int(input('Insert the maximum population size: '))
    maxgen = int(input('Insert the maximum number of generations to simulate: '))
except ValueError:
    print('Please insert an integer.')
    exit(1)
else:
    if (maxpop < 10):
        print('Please choose a population size between 9 and 100000.')
        exit(1)
    if (maxgen < 51):
        print('Please choose a simulation time greater than 50 (up to roughly 275).')
        exit(1)
simulate(maxpop, maxgen)
from collections import Counter
import matplotlib.pyplot as plt

###### FUNCTIONS TO COMPUTE THE STATE OF A PHOTONIC QUANTUM CIRCUIT ######
def readSetup(setup):
    for ii, source in enumerate(setup):
        print(f'Source {ii} emits a photon in mode {source[2]} to path {source[0]} and mode {source[3]} to path {source[1]} with amplitude {source[4]}')

def findPerfectMatchings(graph, store, match=[], edges_left=None):
    if edges_left is None: edges_left = len(set(sum((edge[:2] for edge in graph), [])))//2 # initialize to half of the number of vertices
    if len(graph) > 0:
        #find a vertex number for which the degree is the smallest (big speedup)
        counter_verts = Counter(sum(([edge[0], edge[1]] for edge in graph), []))
        min_degree_vert = min(zip(counter_verts.keys(), counter_verts.values()), key=lambda x: x[1])[0]
        edges_connected = [edge for edge in graph if (edge[0] == min_degree_vert) or (edge[1] == min_degree_vert)]
        for edge in edges_connected:
            reduced_graph = [e for e in graph if not ((e[0] in edge[:2]) or (e[1] in edge[:2]))]
            findPerfectMatchings(reduced_graph, store, match + [edge], edges_left - 1) # go deeper
    elif len(graph) == 0 and edges_left == 0:
        store.append(sorted(match)) # store the perfect matching
    else:
        pass  # Some nodes are not matched and never will

def buildState(setup):
    perfect_matchings = []
    #perfect matchings refer to collections of pair sources for which each path/detector receives exactly one photon
    findPerfectMatchings(setup, perfect_matchings)
    path_count = len(set(sum((source[:2] for source in setup), [])))
    state_dict = {} # ket: amplitude
    for pm in perfect_matchings:
        ket = [0]*path_count
        amplitude = 1 #product of source amplitudes
        for source in pm:
            ket[source[0]], ket[source[1]] = str(source[2]), str(source[3])
            amplitude *= source[4]
        ket = ''.join(ket)
        state_dict[ket] = state_dict.get(ket, 0) + amplitude
    #remove all kets with amplitude 0 and sort the dictionary by key
    state_dict = {key: value for key, value in state_dict.items() if value != 0}
    state_dict = dict(sorted(state_dict.items()))
    #normalize the amplitudes
    total_amplitude = sum(abs(value)**2 for value in state_dict.values())**0.5
    state_dict = {key: value/total_amplitude for key, value in state_dict.items()}

    #factor out ancilla photons (how many of the last photons match in all kets)
    ancilla_photons = 0
    for i in range(1, path_count):
        if len(set([key[-i:] for key in state_dict.keys()])) == 1: ancilla_photons = i
        else: break

    #build state string for output
    state_str = ''
    if ancilla_photons > 0: state_str += '('
    for key, value in state_dict.items():
        if value > 0: state_str += '+'
        state_str += f'{value:.3f}|{key[:path_count-ancilla_photons]}⟩'
    if ancilla_photons > 0: state_str += f')⊗|{ket[-ancilla_photons:]}⟩'
    print(state_str)
    return state_str

def plotSetup(pair_sources, file_name='setup.png'):
    path_count = len(set(sum((source[:2] for source in pair_sources), [])))
    #plot path_count vertical lines, each line represents a path
    plt.figure(figsize=(2+0.5*path_count, 2+0.2*len(pair_sources)))
    for i in range(path_count):
        plt.axvline(x=i, color='black')
    colors = ['red', 'green', 'blue', 'orange', 'pink', 'brown'] + list(plt.cm.viridis(range(256)))
    for ii, source in enumerate(pair_sources):
        plt.plot([source[0], source[0]+(source[1]-source[0])/2], [-ii, -ii], 'o-', color=colors[source[2]], linewidth=8, markersize=0)
        plt.plot([source[1], source[0]+(source[1]-source[0])/2], [-ii, -ii], 'o-', color=colors[source[3]], linewidth=8, markersize=0)
        plt.plot(source[1], -ii, 'k*', markersize=10) #mark the path that the photon is sent to with a star
        plt.plot(source[0], -ii, 'k*', markersize=10) #mark the path that the photon is sent with a star
        if source[4] < 0: plt.plot(source[0]+(source[1]-source[0])/2, -ii, 'kd', markersize=8, markerfacecolor='white') #mark negative amplitudes with white diamond
    plt.yticks([])
    plt.xticks(range(path_count))
    plt.xlabel('Paths')
    plt.savefig(file_name)

# adding a photon pair source to the list of sources
# emitting a pair of photons in mode1 and mode2 to path1 and path2 with a relative amplitude
def C(path1, path2, mode1, mode2, amplitude):
    pair_sources.append([path1, path2, mode1, mode2, amplitude])


###### EXAMPLE: d-DIMENSIONAL GHZ STATE ######
# setup of pair-sources for 3+k dimensional GHZ state (k>=0) with 4 particles, requires 4*k ancilla photons
k = 1
pair_sources = []

C(0,1,0,0,1) #function to create a pair source sending a pair of photons to the first two paths (0 and 1) with mode 0
C(2,3,0,0,1)
C(0,2,1,1,1)
C(1,3,1,1,1)
C(0,3,2,2,1)
C(1,2,2,2,1)
for i in range(k): #for higher dimensions, we need to create more pair sources and ancilla detectors
    dim = 3 + i
    anc1 = 4 + 4*i
    anc2 = 5 + 4*i
    anc3 = 6 + 4*i
    anc4 = 7 + 4*i

    C(anc1, anc2, dim, dim, 1)
    C(anc3, anc4, dim, dim, 1)
    C(anc1, anc3, dim, dim, 1)
    C(anc2, anc4, dim, dim, 1)

    C(anc1, 3, dim, dim, 1)
    C(anc4, 1, dim, dim, 1)

    C(anc3, 0, dim, dim, 1)
    C(anc2, 2, dim, dim, 1)
    C(anc2, 0, dim, dim, -1) #negative amplitudes, necessary for destructive interference
    C(anc3, 2, dim, dim, -1)

# readSetup(pair_sources) #uncomment to print the setup
print(f'Buidling setup for {3+k} dimensional GHZ state (4 particles + {4*k} ancilla photons)')
print(f'Setup has {len(pair_sources)} pair sources')
buildState(pair_sources) #output the state computed from the setup
print('\n')
plotSetup(pair_sources, 'GHZ_setup.png')

###### EXAMPLE: NON-LOCAL CREATION OF d-DIMENSIONAL BELL STATE ######
# setup for non-local creation of 2k dimensional Bell state (k>=1), requires 2*k ancilla photons
k = 2
pair_sources = []

for i in range(k):
    dim1 = 2*i
    dim2 = 2*i + 1
    anc1 = 2 + 2*i
    anc2 = 3 + 2*i

    C(anc1, anc2, 0, 0, 1)
    C(0, anc1, dim1, 0, 1)
    C(1, anc2, dim1, 0, 1)
    C(0, anc2, dim2, 0, 1)
    C(1, anc1, dim2, 0, 1)

# readSetup(pair_sources) #uncomment to print the setup
print(f'Building {2*k} dimensional Bell state (2 particles + {2*k} ancilla photons)')
print(f'Setup has {len(pair_sources)} pair sources')
buildState(pair_sources) #output the state computed from the setup
plotSetup(pair_sources, 'Bell_setup.png')
print('\n')

##### EXAMPLE: 6 particle source ######
# setup of pair-sources for 2+k dimensional GHZ state (k>=0) with 6 particles, requires 6*k ancilla photons
k = 1
pair_sources = []

C(0,1,0,0,1)
C(2,3,0,0,1)
C(4,5,0,0,1)
C(1,2,1,1,1)
C(3,4,1,1,1)
C(0,5,1,1,1)

for i in range(k):
    dim = 2 + i
    anc1 = 6 + 6*i
    anc2 = 7 + 6*i
    anc3 = 8 + 6*i
    anc4 = 9 + 6*i
    anc5 = 10 + 6*i
    anc6 = 11 + 6*i
    
    offset = 7

    C(anc1, anc5, dim, dim, -1)
    C(anc1, anc4, dim, dim, 1)
    C(anc1, anc6, dim, dim, -1)
    C(anc1, 7-offset, dim, dim, 1)
    C(anc1, 8-offset, dim, dim, -1)
    C(anc2, anc4, dim, dim, 1)
    C(anc2, anc5, dim, dim, -1)
    C(anc2, anc6, dim, dim, -1)
    C(anc2, 7-offset, dim, dim, -1)
    C(anc2, 8-offset, dim, dim, 1)
    C(anc2, 12-offset, dim, dim, -1)
    C(anc3, anc4, dim, dim, -1)
    C(anc3, anc5, dim, dim, 1)
    C(anc3, 12-offset, dim, dim, -1)
    C(anc4, 9-offset, dim, dim, 1)
    C(anc4, 10-offset, dim, dim, 1)
    C(anc5, 9-offset, dim, dim, 1)
    C(anc5, 10-offset, dim, dim, 1)
    C(anc6, 11-offset, dim, dim, 1)

# readSetup(pair_sources) #uncomment to print the setup
print(f'Buidling setup for {2+k} dimensional GHZ state (6 particles + {6*k} ancilla photons)')
print(f'Setup has {len(pair_sources)} pair sources')
buildState(pair_sources) #output the state computed from the setup
plotSetup(pair_sources, 'GHZ6_setup.png')
print('\n')


###### EXAMPLE: 8 particle source ######Œ
# setup of pair-sources for 2+k dimensional GHZ state (k>=0) with 8 particles, requires 8*k ancilla photons
k = 1
pair_sources = []

C(0,1,0,0,1)
C(2,3,0,0,1)
C(4,5,0,0,1)
C(6,7,0,0,1)
C(1,2,1,1,1)
C(3,4,1,1,1)
C(5,6,1,1,1)
C(0,7,1,1,1)

for i in range(k):
    dim = 2 + i
    anc1 = 8 + 8*i
    anc2 = 9 + 8*i
    anc3 = 10 + 8*i
    anc4 = 11 + 8*i
    anc5 = 12 + 8*i
    anc6 = 13 + 8*i
    anc7 = 14 + 8*i
    anc8 = 15 + 8*i
    
    offset = 9

    C(anc1, anc5, dim, dim, 1)
    C(anc1, anc6, dim, dim, -1)
    C(anc1, anc8, dim, dim, -1)
    C(anc1, 11-offset, dim, dim, 1)
    C(anc1, 14-offset, dim, dim, -1)

    C(anc2, anc3, dim, dim, 1)
    C(anc2, anc6, dim, dim, 1)
    C(anc2, anc8, dim, dim, 1)
    C(anc2, 10-offset, dim, dim, 1)
    C(anc2, 15-offset, dim, dim, -1)

    C(anc3, anc4, dim, dim, -1)
    C(anc3, 9-offset, dim, dim, -1)
    C(anc3, 16-offset, dim, dim, -1)

    C(anc4, anc6, dim, dim, -1)
    C(anc4, anc8, dim, dim, -1)
    C(anc4, 10-offset, dim, dim, 1)
    C(anc4, 15-offset, dim, dim, -1)

    C(anc5, anc7, dim, dim, -1)
    C(anc5, 13-offset, dim, dim, 1)
    C(anc5, 16-offset, dim, dim, 1)

    C(anc6, anc7, dim, dim, 1)
    C(anc6, 12-offset, dim, dim, -1)
    
    C(anc7, anc8, dim, dim, 1)
    C(anc7, 11-offset, dim, dim, 1)
    C(anc7, 14-offset, dim, dim, -1)

    C(anc8, 9-offset, dim, dim, 1)
    C(anc8, 12-offset, dim, dim, 1)
    C(anc8, 13-offset, dim, dim, 1)

# readSetup(pair_sources) #uncomment to print the setup
print(f'Buidling setup for {2+k} dimensional GHZ state (8 particles + {8*k} ancilla photons)')
print(f'Setup has {len(pair_sources)} pair sources')
buildState(pair_sources) #output the state computed from the setup
plotSetup(pair_sources, 'GHZ8_setup.png')
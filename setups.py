from collections import Counter

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
        state_str += f'{value:.3f}|{key[:-ancilla_photons]}⟩'
    if ancilla_photons > 0: state_str += f')⊗|{ket[-ancilla_photons:]}>'
    print(state_str)
    return state_str


# adding a photon pair source to the list of sources
# emitting a pair of photons in mode1 and mode2 to path1 and path2 with a relative amplitude
def C(path1, path2, mode1, mode2, amplitude):
    pair_sources.append([path1, path2, mode1, mode2, amplitude])


###### EXAMPLE: d-DIMENSIONAL GHZ STATE ######

# setup of pair-sources for 3+N dimensional GHZ state (N>=0)
N = 3
pair_sources = []

C(0,1,0,0,1) #function to create a pair source sending a pair of photons to the first two paths (0 and 1) with mode 0
C(2,3,0,0,1)
C(0,2,1,1,1)
C(1,3,1,1,1)
C(0,3,2,2,1)
C(1,2,2,2,1)
for i in range(N): #for higher dimensions, we need to create more pair sources and ancilla detectors
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
print(f'Building {3+N} dimensional GHZ state')
print(f'Setup has {len(pair_sources)} pair sources')
buildState(pair_sources) #output the state computed from the setup

print('\n')

###### EXAMPLE: NON-LOCAL CREATION OF d-DIMENSIONAL BELL STATE ######

# setup for non-local creation of 2N dimensional Bell state (N>=1)
N = 2
pair_sources = []

for i in range(N):
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
print(f'Building {2*N} dimensional Bell state')
print(f'Setup has {len(pair_sources)} pair sources')
buildState(pair_sources) #output the state computed from the setup
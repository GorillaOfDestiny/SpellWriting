import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
#So, there are two methods for generating necklaces, my old one which is really bad 
# and another that's presented in this paper:

# https://www.sciencedirect.com/science/article/pii/019667749290047G

# I'm going to try and recreate that algorithm here but it might not work.

def cycle_list(l:list,loops:int = 1):
    """Used to cycle list elements so that everything is one step left

    Args:
        l (list): the list to cycle
        loops (int, optional): The number of steps to do. Defaults to 1.
    """
    n = len(l)
    if loops < 0:
        l = l[::-1]
    for t in range(np.abs(loops)):
        l = [l[(i+1) % n] for i in range(n)]
    if loops < 0:
        l = l[::-1]
    return(l)


def generate_unique_combinations(N,tqdm_disable = True):
    """Old Method

    Args:
        N (int): Number of elements long
    """
    combinations = generate_binary_strings(N)
    non_repeating = [combinations[0]]
    for i in tqdm(range(len(combinations)),desc = "Genearting Unique Binary Numbers",disable = tqdm_disable):
        ref = list(combinations[i])
        N = len(ref)
        test = 0
        for j in range(len(non_repeating)):
            for n in range(N):
                
                if cycle_list(list(non_repeating[j]),loops = n+1) == ref:
                    test += 1
        
        if test == 0:
            non_repeating.append(combinations[i])
            
    for i in np.arange(len(non_repeating)):
        non_repeating[i] = [int(s) for s in list(non_repeating[i])]
    return(non_repeating)

def generate_binary_strings(bit_count):
    """Generates all binary strings of length <bit_count>

    Args:
        bit_count (int): Number of bits

    Returns:
        list: list of binary strings
    """
    binary_strings = []
    def genbin(n, bs=''):
        #not sure this is great but it does work...kinda?
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            genbin(n, bs + '0')
            genbin(n, bs + '1')


    genbin(bit_count)
    return binary_strings

# Now for the new
# I think the idea is to generate a tree. then you keep the tree going if and only if the output is a valid necklace
# though this is not clear to me how we check that.

def tau_fn(binary_list):
    binary_list[-1] = abs(binary_list[-1] -1)
    return(binary_list)

def check_necklace(current_output,candidate,already_checked):
    if candidate[-1] == 0:
        return(False)
    for l in range(len(candidate)):
        if cycle_list(candidate,l) in current_output:
            return(False)
    else:
        return(True)

def check_children(bn,current_output,already_checked,pbar,depth = 0):
    if check_necklace(bn,current_output,already_checked):
        for n in range(1,len(bn)-1):
           
            child = tau_fn(cycle_list(bn,n))
            if check_necklace(current_output,child,already_checked):
                pbar.update(1)
                #print("".join(["\t"]*depth),f"Child {n}: ",child,"Necklace: True")
                current_output.append(child)
                #already_checked.append(child)
                
                current_output,already_checked = check_children(child,current_output,already_checked,pbar,depth = depth + 1)
            else:
                #print("".join(["\t"]*depth),f"Child {n}: ",child,"Necklace: False")
                #already_checked.append(child)
                break
    return(current_output,already_checked)

def bin_to_int(all_binaries):
    binary_strings = ["0b" + "".join([str(ab_) for ab_ in ab]) for ab in all_binaries]
    binary_base_10 = [int(bs,2) for bs in binary_strings]
    return(binary_base_10)
def standardise_binary(b_list):
    # goal here is to make the binary number the lowest it can be
    all_binaries = [cycle_list(b_list,n) for n in range(len(b_list))]

    #this line is super slow so might need updated
    binary_base_10 = bin_to_int(all_binaries)
    return(all_binaries[binary_base_10.index(min(binary_base_10))])

def order_binary(final_output):
    value_list = bin_to_int(final_output)
    final_output = [bn for _, bn in sorted(zip(value_list,final_output))]
    return(final_output)
def generate_unique_necklaces(n,tqdm_disable = True,tqdm_total = 7):

    #assumme tqdm total, need to write code that can calculate this from n

    
    
    #we start at all 0s
    #define binary numbers as lists of values for now
    # I could deal in strings but not necessarily keen to right now
    # therefore 0^n = [0]*n (i.e. 0^2 = [0,0])
    final_output = []
    zero_n = [0]*n
    final_output.append(zero_n) #cause this is a given
    
    with tqdm(total = tqdm_total,disable = tqdm_disable) as pbar:
        final_output,_ = check_children(zero_n,final_output,final_output,pbar = pbar)
        #this step not strictly necessary but it helps with keeping things standard
        final_output = [standardise_binary(b) for b in final_output]
        final_output = order_binary(final_output)
    return(final_output)

#A MUCH better solution

# turns out the "new" method is slow as hell, might be my own code problem
# but Ernesti from the Theory of Magic server has this much nicer method I'll just
# copy. 

# The idea is to generate all possible binaries for the given bit length then check if
# that is the minimum value of that necklace. If so we pass it, if not then we don't

def split_ernesti(all_binaries):
    final_output = [[int(b) for b in list(ab)] for ab in all_binaries]
    return(final_output)

def generate_unique_binaries_ernesti(n = 13):

    #stolen from https://github.com/Ernesti04/necklace_projects/blob/main/necklace_gen_v2.py
    x = 1						# start at 1, avoid all 0s case
    uniques = ["".join(["0"]*n)]
    while (x < 2**n): 			# for each possible number
        s = str(bin(x)[2:].zfill(n)) 	# get binary of number
        cycle = [] 				# get blank list to check rotations
        for i in range(len(s)-1): 	# for each bit in the sequence
            #rot = cycle[i][-1] + cycle[i][:-1] #slightly slower
            rot = s[i:] + s[:i] 		# rotate by i bits
            cycle.append(rot) 		# add each rotation
            if rot < s : 				# if rotation found that is smaller
                break 				# stop searching
        if min(cycle) == s : 		# if the number is already minimum
            uniques.append(s) 		# add to the list
            #print(f'\t{s}') # print results (slow)
        x += 2 					# count odds, halves time
    uniques = split_ernesti(uniques)
    return(uniques)

def default_generation(n = 13):
    return(generate_unique_binaries_ernesti(n))

if __name__ == "__main__":
    import timeit
    
    N = 8
    t_start = timeit.default_timer()
    new_N = generate_unique_necklaces(N,tqdm_disable=False)
    t_end = timeit.default_timer()
    print(f"New Method: {(t_end - t_start):.1g}s | n_uniques = {len(new_N)}")

    t_start = timeit.default_timer()
    old_N = generate_unique_combinations(N,tqdm_disable=False)
    t_end = timeit.default_timer()
    print(f"Old Method: {(t_end - t_start):.1g}s | n_uniques = {len(old_N)}")

    


    # The result is that the ernesti method works best and so we will use that. It is based off the 
    # Lyndon word algorithm if you're curious for futher reading
    
    t_start = timeit.default_timer()
    old_N = generate_unique_binaries_ernesti(N)
    t_end = timeit.default_timer()
    print(f"Ernesti Method, Generating for {N}-length binaries: {(t_end - t_start):.3g}s | n_uniques = {len(old_N)}")
    


    #CURRENT EXPERIMENTS
    # IF we wanted to push this even faster (which would be silly) we could skip numbers over (2^N)/2
    #   because only the last number shows up there. Ernesti's algo is fast enough I don't think it's
    #   necessary but in some ways it's fun just to push it to the absolute limit.


    # for N in np.arange(50):
    #     N = 5
    #     old_N = generate_unique_binaries_ernesti(N)
    #     old_N_vals = [int("".join([str(b) for b in bn]),2) for bn in old_N]
    #     all_binaries = [0]
    #     for x in np.arange(1,2**(N)):
    #         s = str(bin(x)[2:].zfill(N))
    #         all_binaries.append(s)

    #     onv = np.array(old_N_vals)

    #     print(len(np.where(onv >= (2**N)//2)[0]))
    # for i in range(2**N):
    #     filler = str(all_binaries[i])
    #     if i in old_N_vals:
    #         filler += "<-"
    #     if i == 2**N//2:
    #         filler += "------"
    #     print(f'{i}: {filler}')
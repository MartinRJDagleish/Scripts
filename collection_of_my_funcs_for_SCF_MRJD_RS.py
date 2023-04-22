def valid_permut(i,j,k,l):
    i,j,k,l = str(i),str(j),str(k),str(l)
    permuts = []
    permuts.append(i+j+k+l)
    permuts.append(j+i+k+l)
    permuts.append(i+j+l+k)
    permuts.append(j+i+l+k)
    permuts.append(k+l+i+j)
    permuts.append(l+k+i+k)
    permuts.append(k+l+j+i)
    permuts.append(l+k+j+i)
    return permuts
    
def check_ERIs(my_array: np.ndarray, ERI):
    for i in range(no_basis_funcs):
        for j in range(i):
            for k in range(j):
                for l in range(k):
                    J_idx = calc_ijkl_idx(i,j,k,l)
                    K_idx = calc_ijkl_idx(i,k,j,l)
                    is_J_int_same = round(my_array[J_idx],4) == round(ERI[(i,j,k,l)],4)
                    is_K_int_same = round(my_array[K_idx],4) == round(ERI[(i,k,j,l)],4)
                    if is_J_int_same or is_K_int_same:
                    print(f"{i,j,k,l}:{J_idx},{K_idx}")
                    print(f"mJ_int:{my_array[J_idx]}, c_Jint:{ERI[(i,j,k,l)]}, mK_int:{my_array[K_idx]}, c_K_int:{ERI[(i,k,j,l)]}\n")
                    
def calc_ijkl_idx(i: int, j: int, k: int, l: int) -> int:
   ij = calc_cmp_idx(i,j) if i > j else calc_cmp_idx(j,i)
   kl = calc_cmp_idx(k,l) if k > l else calc_cmp_idx(l,k)
   ijkl = calc_cmp_idx(ij,kl) if ij > kl else calc_cmp_idx(kl,ij)
   return ijkl                    
   
def calc_cmp_idx(idx1: int, idx2: int) -> int:
   return int(idx1 * (idx1 + 1) / 2 + idx2)
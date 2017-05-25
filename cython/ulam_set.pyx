cdef int infinity_norm(v):
    return max(abs(v[0]), abs(v[1]))

cdef int two_norm_squared(v):
    return v[0]**2 + v[1]**2


cdef vector_sum(v, w):
    return (v[0]+w[0], v[1]+w[1])


cpdef compute_ulam_set(int n, init_vectors=[(1, 0), (0, 1)], norm=infinity_norm):
    # ulam_set is the set of all ulam elements found so far
    ulam_set = set(init_vectors)

    # new_ulam is the set of all ulam elements found in the latest iteration
    new_ulam = set(init_vectors)

    # pairwise sums is the set of all pairwise sums of all ulam elements found
    # so far that are not already in ulam_set
    pairwise_sums = set([])

    cdef i
    for i in range(n):
        # update pairwise sums by computing pairwise sums between new_ulam
        # elements and ulam_set elements and substracting ulam_set
        new_sums = [vector_sum(x, y) for x in ulam_set for y in new_ulam
                    if x != y]
        pairwise_sums = pairwise_sums.union(new_sums)
        pairwise_sums = pairwise_sums.difference(ulam_set)

        # update new_ulam to be the set of pairwise sums of smallest norm
        smallest_norm = min([norm(x) for x in pairwise_sums])
        new_ulam = set([x for x in pairwise_sums if norm(x) == smallest_norm])

        # update ulam_set to include new_ulam
        ulam_set = ulam_set.union(new_ulam)

    return ulam_set

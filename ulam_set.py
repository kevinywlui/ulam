from sys import argv


def infinity_norm(v):
    return max(abs(v[0]), abs(v[1]))


def two_norm_squared(v):
    return v[0]**2 + v[1]**2


def vector_sum(v, w):
    return (v[0]+w[0], v[1]+w[1])


def compute_ulam_set(n, init_vectors=[(1, 0), (0, 1)], norm=infinity_norm):
    init_sum = vector_sum(*init_vectors)

    # new_ulam is the set of all ulam elements found at the latest iteration
    new_ulam = set([init_sum])

    # old_ulam is the set of all ulam elements found prior to the latest
    # iteration
    old_ulam = set(init_vectors)

    # ulam_set is the union of old and new
    ulam_set = new_ulam.union(old_ulam)

    # pairwise_sums is the set of all pairwise sums ever generated
    pairwise_sums = ulam_set.copy()

    # candidates is the set of possibly new ulam_elements
    candidates = set()

    for _ in range(n):
        # new_old_sums is all pairwise sums of an old_ulam element with a
        # new_ulam element
        new_old_sums = [vector_sum(x, y) for x in new_ulam for y in old_ulam]

        # new_new_sums is all pairwise sums of a new_ulam element with a
        # new_ulam_element
        new_new_sums = [vector_sum(x, y) for x in new_ulam for y in new_ulam
                        if x!=y]

        candidates = candidates.union(new_old_sums)
        candidates = candidates.union(new_new_sums)

        seen_new_old = set()
        for x in new_old_sums:
            # this means x is a dup
            if x in seen_new_old or x in pairwise_sums:
                try:
                    candidates.remove(x)
                except KeyError:
                    pass
                seen_new_old.add(x)
            # this means x is new
            else:
                seen_new_old.add(x)

        seen_once_new_new = set()
        seen_twice_new_new = set()
        for x in new_new_sums:
            # this means x is an old dup
            if x in pairwise_sums:
                try:
                    candidates.remove(x)
                except KeyError:
                    pass
            # unique sums will appear exactly twice in new_new
            elif x in seen_once_new_new:
                seen_once_new_new.remove(x)
                seen_twice_new_new.add(x)
            elif x in seen_twice_new_new:
                try:
                    candidates.remove(x)
                except KeyError:
                    pass
            # this means x is new
            else:
                seen_once_new_new.add(x)

        pairwise_sums = pairwise_sums.union(new_old_sums)
        pairwise_sums = pairwise_sums.union(new_new_sums)

        smallest_norm = min([norm(x) for x in candidates])
        new_ulam = set([x for x in candidates if norm(x)==smallest_norm])
        old_ulam = ulam_set
        ulam_set = new_ulam.union(old_ulam)
        candidates = candidates.difference(new_ulam)

    return ulam_set

try:
    m = int(argv[1])
except:
    m = 10
ulam = sorted(compute_ulam_set(m))
print(ulam)
print(len(ulam))

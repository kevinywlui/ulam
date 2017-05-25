from ulam_set import compute_ulam_set
from sys import argv

try:
    m = int(argv[1])
except:
    m = 100
ulam = compute_ulam_set(m)
print(len(ulam))
print(ulam)

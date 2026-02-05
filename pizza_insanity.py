import math
from itertools import combinations

e = math.e
N = 102

raw_seq = [1 + int(e * n) % N for n in range(1, N + 1)]

print("RAW SEQUENCE:")
print(raw_seq)
print(f"Length: {len(raw_seq)}\n")

counts = {}
reduced_seq = []
for val in raw_seq:
    if counts.get(val, 0) < 3:
        reduced_seq.append(val)
        counts[val] = counts.get(val, 0) + 1

print("REDUCED SEQUENCE:")
print(reduced_seq)
print(f"Length: {len(reduced_seq)}\n")

slices = [tuple(reduced_seq[i*3:(i+1)*3]) for i in range(len(reduced_seq)//3)]
print(f"PIZZA SLICES ({len(slices)}):")
for i, s in enumerate(slices):
    print(f"  {i}: {s}")

def rotations(t):
    return [(t[0],t[1],t[2]), (t[1],t[2],t[0]), (t[2],t[0],t[1])]

def solve(slices):
    n = len(slices)

    def bt(idx, used, cols):
        if idx == n:
            return []
        for r in rotations(slices[idx]):
            ok = all(r[j] not in cols[j] for j in range(3))
            if ok:
                for j in range(3):
                    cols[j].add(r[j])
                rest = bt(idx+1, used|{idx}, cols)
                if rest is not None:
                    return [(idx, r)] + rest
                for j in range(3):
                    cols[j].remove(r[j])
        return None

    return bt(0, set(), [set(), set(), set()])

def minimal_obstacle(slices):
    for sz in range(2, len(slices)+1):
        for combo in combinations(range(len(slices)), sz):
            sub = [slices[i] for i in combo]

            def bt(idx, cols):
                if idx == len(sub):
                    return True
                for r in rotations(sub[idx]):
                    ok = all(r[j] not in cols[j] for j in range(3))
                    if ok:
                        for j in range(3):
                            cols[j].add(r[j])
                        if bt(idx+1, cols):
                            return True
                        for j in range(3):
                            cols[j].remove(r[j])
                return False

            if not bt(0, [set(), set(), set()]):
                return combo, sub
    return None, None

print("\n" + "="*50)
print("SOLVING...\n")

sol = solve(slices)
if sol:
    print("SOLUTION (column of triples):")
    for idx, triple in sol:
        print(f"  {triple}")
else:
    print("NO SOLUTION EXISTS\n")
    obs_idx, obs = minimal_obstacle(slices)
    if obs_idx:
        print(f"MINIMAL OBSTACLE (indices {obs_idx}):")
        for i, s in zip(obs_idx, obs):
            print(f"  Slice {i}: {s}")

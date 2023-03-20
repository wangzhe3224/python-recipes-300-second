from collections import defaultdict


d = {
    "a": 1, 
    "b": 1,
    "c": 2,
}

reverse = defaultdict(list)
for k, v in d.items():
    reverse[v].append(k)

print(f"{d = }")
print(f"{reverse = }")
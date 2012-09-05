#problem olymp
n = int(input())
points = [int(x) for x in input().split()]
ids = [i for i in range(n)]

for i in range(n):
	for j in range(n - i - 1):
		if points[j + 1] > points[j]:
			points[j], points[j + 1] = points[j + 1], points[j]
			ids[j], ids[j + 1] = ids[j + 1], ids[j]

print(' '.join([str(x + 1) for x in ids]))

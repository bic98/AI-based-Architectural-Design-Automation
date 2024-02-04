def normalize_sizes(sizes, dx, dy):
    total_size = sum(sizes)
    total_area = dx * dy
    sizes = map(float, sizes)
    sizes = map(lambda size: size * total_area / total_size, sizes)
    return list(sizes)

size = [4, 5, 12, 4, 2]
x = 12
y = 10

k = normalize_sizes(size, x, y)
print(k)
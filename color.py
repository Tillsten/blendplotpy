colors = {}
with open("color.txt") as f:
    f.readline()
    for l in f.readlines():
        idx = l.find("#")
        name = l[:idx - 1]
        color = l[idx + 1:-2]
        color = int(color, base=16)
        colors[name] = color
del color

from pathlib import Path

colors = {}
with open(Path(__file__).parent / "color.txt") as f:
    f.readline()
    for l in f.readlines():
        idx = l.find("#")
        name = l[:idx - 1]
        color = 'ff' + l[idx + 1:-2]
        color = int(color, base=16)
        colors[name] = color
del color

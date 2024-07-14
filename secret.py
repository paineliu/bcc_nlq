def get_secret_key(filename):
    f = open(filename)
    line = f.readline()
    items = line.strip().split()
    if len(items) == 2:
        return items[0], items[1]
    else:
        return "", items[0]
    
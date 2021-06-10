def format_dict(data, delim=",", sep="=", brackets=True):
    data_str = "{" if brackets else ""
    delim_str = ""
    for variable, value in data.items():
        data_str += f"{delim_str}{variable}{sep}{value}"
        delim_str = f"{delim} "
    data_str += "}" if brackets else ""
    return f"{data_str}"


def powerset_dict(data):  # https://stackoverflow.com/a/1482320
    n = len(data)
    masks = [1 << i for i in range(n)]
    for i in range(1 << n):
        yield {key: data[key] for mask, key in zip(masks, data) if i & mask}


def powerset_set(data):  # https://stackoverflow.com/a/1482320
    n = len(data)
    masks = [1 << i for i in range(n)]
    for i in range(1 << n):
        yield {element for mask, element in zip(masks, data) if i & mask}

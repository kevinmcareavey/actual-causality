def format_dict(data, delim=",", sep="=", brackets=True):
    data_str = "{" if brackets else ""
    delim_str = ""
    for variable, value in data.items():
        data_str += f"{delim_str}{variable}{sep}{value}"
        delim_str = f"{delim} "
    data_str += "}" if brackets else ""
    return f"{data_str}"


def powerset_dict(d):  # https://stackoverflow.com/a/1482320
    n = len(d)
    masks = [1 << i for i in range(n)]
    for i in range(1 << n):
        yield {key: d[key] for mask, key in zip(masks, d) if i & mask}

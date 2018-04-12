def startswith(lexis_string, pattern):
    position = 0

    for p in pattern:
        if position >= len(lexis_string):
            return False

        for e in lexis_string[position]:
            if p == e:
                position += len(e.string)
                break
        else:
            return False
    return True


def endswith(lexis_string, pattern):
    return len(lexis_string) >= len(pattern) \
           and all(lexis_string[-i - 1] == pattern[-i - 1] for i in range(len(pattern)))


def split(lexis_string, separator):
    result = [[]]

    for e in lexis_string:
        if e == separator:
            result.append([])
        else:
            result[-1].append(e)

    return result

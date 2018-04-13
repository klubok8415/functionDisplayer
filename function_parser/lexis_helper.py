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
    position = 0

    for p in pattern[::-1]:
        if position >= len(lexis_string):
            return False

        for e in lexis_string[-position - 1]:
            if p == e:
                position += len(e.string)
                break
        else:
            return False
    return True


def split(lexis_string, separator):
    result = [[]]

    position = 0
    while position < len(lexis_string):
        if separator in lexis_string[position]:
            result.append([])
        else:
            result[-1].append(lexis_string[position])
        position += 1

    return result

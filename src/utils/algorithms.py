def quick_select(values, k, pivot_fn, index=0):
    """
    Select the kth element in values (0 based)
    :param values: an Iterable object
    :param k: Index
    :param pivot_fn: Function to choose a pivot, defaults to random.choice
    :param index: the position of the iterable to compare
    :return: The kth element of values
    """
    if len(values) == 1:
        assert k == 0
        return values[0]
    pivot = pivot_fn(values)

    lows, highs, equals = [], [], []
    for elem in values:
        e_value, p_value = elem[index], pivot[index]
        if e_value < p_value:
            lows.append(elem)
        elif e_value > p_value:
            highs.append(elem)
        else:
            equals.append(elem)

    if k < len(lows):
        return quick_select(lows, k, pivot_fn, index=index)
    elif k < len(lows) + len(equals):
    # We got lucky and guessed the median
        return equals[0]
    else:
        return quick_select(highs, k - len(lows) - len(equals), pivot_fn, index=index)

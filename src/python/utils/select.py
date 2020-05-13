import random

def quick_select_median(values, pivot_fn=random.choice):
        k = len(values) // 2
        return quick_select(values, k, pivot_fn)


def quick_select(values, k, pivot_fn):
    if len(values) == 1:
        assert k == 0
        return values[0]
    pivot = pivot_fn(values)

    lows, highs, equals = [], [], []
    for elem in values:
        if elem < pivot:
            lows.append(elem)
        elif elem > pivot:
            highs.append(elem)
        else:
            equals.append(elem)

    if k < len(lows):
        return quick_select(lows, k, pivot_fn)
    elif k < len(lows) + len(equals):
        # We got lucky and guessed the median
        return equals[0]
    else:
        return quick_select(highs, k - len(lows) - len(equals), pivot_fn)

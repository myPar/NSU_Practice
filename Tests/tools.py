
# check equality double numbers with accuracy
def is_close(val1, val2, accuracy) -> bool:
    if abs(val1 - val2) > accuracy:
        return False
    else:
        return True

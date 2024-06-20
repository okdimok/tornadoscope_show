# this function returns a minimal dictionary d, such that 
# b == {**a, **d}
def dictdiff(a, b):
    diff = set(b.items()) - set(a.items())
    return dict(diff)

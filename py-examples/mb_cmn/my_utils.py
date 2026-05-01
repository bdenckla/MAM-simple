"""
Exports various functions of general utility.
"""

from functools import reduce
from itertools import groupby


def init_at_key(dic, key, val):
    """If key is fresh in dic, set its value to val. Otherwise assert."""
    assert key not in dic
    dic[key] = val


def maybe_init_at_key(dic, key, val):
    """If key is fresh in dic, set its value to val. Otherwise whiff."""
    if key not in dic:
        dic[key] = val


def increment_at_key(dic, key, val=1):
    maybe_init_at_key(dic, key, 0)
    dic[key] += val


def append_at_key(dic, key, val):
    maybe_init_at_key(dic, key, [])
    dic[key].append(val)


def first_and_only(seq):
    """Assert that this is there is only 1 el of seq, and returns it."""
    assert len(seq) == 1
    return seq[0]


def first_and_only_and_str(seq):
    """Like first_and_only, but also asserts that result is a string."""
    fao = first_and_only(seq)
    assert isinstance(fao, str)
    return fao


def tuplify(obj):
    if isinstance(obj, (tuple, list)):
        return st_map(tuplify, obj)
    return obj


def szip(*seqs):
    """Strongly zip (zip, asserting equal length)"""
    for seq in seqs[1:]:
        assert _len_for_szip(seq) == _len_for_szip(seqs[0])
    return zip(*seqs)


def l_szip(*seqs):
    """Force output of szip to be a list."""
    return list(szip(*seqs))


def intersperse(sep, the_sequence):
    """
    Intersperse a separator between the elements of a sequence.
    intersperse(7,[0, 1, 2]) == [0, 7, 1, 7, 2]
    intersperse(7,(0, 1, 2)) == (0, 7, 1, 7, 2)
    """
    assert isinstance(the_sequence, (tuple, list))
    type_of_seq = type(the_sequence)  # presumably list or tuple
    seps = type_of_seq([sep]) * len(the_sequence)
    tmp_list = sum_of_seqs(szip(the_sequence, seps))
    tmp = type_of_seq(tmp_list)
    return tmp[:-1]  # rm final sep, e.g. final None


def sl_map(foc, the_sequence):
    """
    Map the given foc (function or closure) over the given sequence (e.g. list or tuple).
    (The "sl" means "[any] sequence in, list out".)
    """
    if isinstance(foc, tuple):
        return [foc[0](*foc[1:], elem) for elem in the_sequence]
    return list(map(foc, the_sequence))


def sum_of_map(foc, the_sequence):
    return sum_of_seqs(sl_map(foc, the_sequence))


def st_map(foc, the_sequence):
    """
    Map the given foc (function or closure) over the given sequence (e.g. list or tuple).
    (The "st" means "[any] sequence in, tuple out".)
    """
    if isinstance(foc, tuple):
        return tuple(foc[0](*foc[1:], elem) for elem in the_sequence)
    return tuple(map(foc, the_sequence))


def ss_map(foc, the_sequence):
    """
    Map the given foc (function or closure) over the given sequence (e.g. list or tuple).
    (The "ss" means "[any] sequence in, [same type of] sequence out [as in]".)
    (I.e. tuple in, tuple out or list in, list out.)
    """
    type_of_seq = type(the_sequence)  # presumably list or tuple
    if isinstance(foc, tuple):
        return type_of_seq(foc[0](*foc[1:], elem) for elem in the_sequence)
    return type_of_seq(map(foc, the_sequence))


def dv_dispatch(fn_table, dic):
    """
    Return a dict with the same keys but with values mapped according to a dict of functions.
    {k: v} becomes {k: f[k](v)}
    """
    return {k: fn_table[k](v) for k, v in dic.items()}


def dv_map(foc, the_dic):
    """
    "Dictionary value map"
    Return a dict with the same keys but with values mapped.
    {k: v} becomes {k: f(v)}
    """
    assert isinstance(the_dic, dict)
    if isinstance(foc, tuple):
        return {k: foc[0](*foc[1:], v) for k, v in the_dic.items()}
    return {k: foc(v) for k, v in the_dic.items()}


def dk_map(foc, the_dic):
    """
    "Dictionary key map"
    Return a dict with the same values but with the keys mapped.
    {k: v} becomes {f(k): v}
    """
    assert isinstance(the_dic, dict)
    if isinstance(foc, tuple):
        return {foc[0](*foc[1:], k): v for k, v in the_dic.items()}
    return {foc(k): v for k, v in the_dic.items()}


def dkv_map(foc, the_dic):
    """
    "Dictionary key and value map"
    Return a dict with the same keys but with values mapped.
    {k: v} becomes {k: f(k, v)}
    """
    assert isinstance(the_dic, dict)
    if isinstance(foc, tuple):
        return {k: foc[0](*foc[1:], k, v) for k, v in the_dic.items()}
    return {k: foc(k, v) for k, v in the_dic.items()}


def snd_map(foc, the_seq):
    """
    "Second value map"
    [(x, y)] becomes [(x, f(y))].
    """
    if isinstance(foc, tuple):
        return [(x, foc[0](*foc[1:], y)) for x, y in the_seq]
    return [(x, foc(y)) for x, y in the_seq]


def sl_map_even_odd(foc_pair, the_sequence):
    """Like sl_map, but with a different foc for even- & odd-indexed elements."""
    return sl_map((_even_odd_foc, foc_pair), enumerate(the_sequence))


def my_groupby(iterable, keyfunc):
    # I used to implement this using itertools.groupby.
    # But it does something different than what we need.
    # If input=[(1, 10), (1, 11), (2, 12), (1, 13)]
    # and output=[(x, list(y)) for x,y in groupby(input, lambda z: z[0])],
    # then output is a list having the following values:
    #    (1, [(1, 10), (1, 11)]),
    #    (2, [(2, 12)]),
    #    (1, [(1, 13)])
    out = {}
    for elem in iterable:
        append_at_key(out, keyfunc(elem), elem)
    return out


def sum_of_seqs(seq_of_seqs):
    """
    Return a list that is the sum of a sequence of sequences.
    Aka "flatten".
    The seq_of_seqs arg can be a tuple or a list.
    The seqs inside it can be tuples, lists, or any mix of the two.
    E.g. all of the following yield [1, 2, 3, 4]:
        sum_of_seqs([[1, 2], [3, 4]]) (list of lists)
        sum_of_seqs([(1, 2), (3, 4)]) (list of tuples)
        sum_of_seqs([(1, 2), [3, 4]]) (list of mix)
        sum_of_seqs(((1, 2), [3, 4])) (tuple of mix)
    """
    accum = []
    for seq in seq_of_seqs:
        accum.extend(seq)
    return accum


def sum_of_tuples(seq_of_tuples):
    """
    Return a tuple that is the sum of a sequence of tuples.
    Aka "flatten".
    The seq_of_seqs arg can be a tuple or a list.
    The elements inside it must all be tuples though.
    """
    accum = tuple()
    for the_tuple in seq_of_tuples:
        accum += the_tuple
    return accum


def sum_of_dics(seq_of_dics):
    return reduce(_accum_dic, seq_of_dics)


def _even_odd_foc(foc_pair, idx_and_elem):
    idx, elem = idx_and_elem
    foc = foc_pair[idx % 2]
    if isinstance(foc, tuple):
        return foc[0](*foc[1:], elem)
    return foc(elem)


def _accum_dic(accum, dic):
    return {**accum, **dic}


def _len_for_szip(obj):
    if not isinstance(obj, (tuple, list)):
        return len(tuple(obj))
    return len(obj)

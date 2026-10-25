"""Adaptive RPS player. Prepared with AI assistance for an agentic AI assignment."""

from collections import Counter, defaultdict
from itertools import permutations

MOVES = 'RPS'
BEATS = {'R': 'P', 'P': 'S', 'S': 'R'}


def _predictions(ours, theirs):
    last = ours[-1] if ours else 'R'
    predictions = {'response_to_last': BEATS[last]}

    frequencies = Counter(ours[-10:] or ['S'])
    for order in permutations(MOVES):
        common = max(order, key=lambda move: frequencies[move])
        predictions['frequency_' + ''.join(order)] = BEATS[common]

    # Predict opponents that model transitions between our previous moves.
    transitions = defaultdict(Counter)
    sequence = ['R'] + ours
    for before, after in zip(sequence, sequence[1:]):
        transitions[before][after] += 1
    expected = max(MOVES, key=lambda move: transitions[last][move])
    predictions['response_to_transition'] = BEATS[expected]

    for period in range(1, 11):
        predictions[f'period_{period}'] = (
            theirs[-period] if len(theirs) >= period else 'R'
        )

    # Learn recurring suffixes in the opponent's own moves.
    for width in range(1, 7):
        counts = Counter()
        if len(theirs) > width:
            suffix = theirs[-width:]
            for index in range(len(theirs) - width):
                if theirs[index:index + width] == suffix:
                    counts[theirs[index + width]] += 1
        predictions[f'pattern_{width}'] = max(MOVES, key=lambda move: counts[move])
    return predictions


def player(prev_play, _state={}):
    """Return a move, resetting match state when prev_play is empty."""
    if not prev_play or not _state:
        _state.clear()
        _state.update(ours=[], theirs=[], scores={}, predictions={})
    else:
        _state['theirs'].append(prev_play)
        for name, guess in _state['predictions'].items():
            _state['scores'][name] = (
                0.97 * _state['scores'].get(name, 0.0) + (guess == prev_play)
            )

    predictions = _predictions(_state['ours'], _state['theirs'])
    best = max(predictions, key=lambda name: _state['scores'].get(name, 0.0))
    move = BEATS[predictions[best]]
    _state['predictions'] = predictions
    _state['ours'].append(move)
    return move

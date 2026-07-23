# transposition.py

from dataclasses import dataclass


@dataclass
class TTEntry:
    """
    A single entry in the transposition table.
    """

    depth: int
    score: int
    flag: str
    best_move: object = None


class TranspositionTable:
    """
    Simple transposition table.
    """

    EXACT = "EXACT"
    LOWERBOUND = "LOWERBOUND"
    UPPERBOUND = "UPPERBOUND"

    def __init__(self):
        self.table = {}

    def clear(self):
        """
        Remove all stored positions.
        """
        self.table.clear()

    def store(self, zobrist_key, depth, score, flag, best_move=None):
        """
        Save a position in the table.
        """

        self.table[zobrist_key] = TTEntry(
            depth=depth,
            score=score,
            flag=flag,
            best_move=best_move
        )

    def lookup(self, zobrist_key):
        """
        Return the stored entry if it exists.
        """

        return self.table.get(zobrist_key)

    def contains(self, zobrist_key):
        """
        Check if a position exists.
        """

        return zobrist_key in self.table

    def size(self):
        """
        Number of stored positions.
        """

        return len(self.table)
"""Statement processing for the adventure game."""

from typing import Union, Optional, Tuple
from adventure.commands.command import Command
from adventure.commands.command_list import CommandList
from adventure.exceptions import BadStatementError, CommandNotFoundError
from adventure.constants import PREPOSITIONS, SEPARATORS

class Statement:
    """A statement class to process the statements given by the player."""

    def __init__(self, statement: str = None, cmd_list: CommandList = None) -> None:
        if not statement:
            raise BadStatementError("No statement given")
        self.stmt = statement
        self.action: str = ""
        self.tokens: list[str] = statement.split()
        try:
            self.verb: Command = self.identify_verb(self.tokens, cmd_list)
        except CommandNotFoundError as e:
            raise CommandNotFoundError from e
        if not self.verb:
            raise CommandNotFoundError("No valid command found.")
        # self.object: list[str] = self.identify_objects(self.tokens)
        # self.mods: list[str] = self.identify_modifiers(self.tokens)
        # Probably deprecated
        self.args: list[str] = self.identify_args()

    def identify_verb(
        self, tokens: list[str], commands: CommandList
    ) -> Union[Command, None]:
        """Identify the verb in the statement.

        Args:
            tokens (list[str]): The list of tokens from the statement.
            commands (list[str]): The list of available command names and aliases.

        Returns:
            Union[str, None]: The token with a valid command name or
                None if not found.

        """
        if not tokens:
            raise BadStatementError("No tokens to identify verb from")
        if not commands:
            raise CommandNotFoundError("No commands available to match verb")
        for token in tokens:
            for command in commands:
                if token == command.name or token in command.aliases:
                    self.action = token
                    return command
        return None

    def identify_args(self) -> list[str]:
        """Separate the args from the verb in the statement."""
        self.args = [token for token in self.tokens if token != self.action]
        return self.args

    class _TrieNode:
        __slots__ = ("children", "value")

        def __init__(self):
            self.children: dict[str, "Statement._TrieNode"] = {}
            self.value: Optional[str] = None  # store candidate string when a word sequence ends here

    def _build_trie(self, candidates: list[str]) -> "_TrieNode":
        """Build a trie of tokenized candidate names (lowercased)."""
        root = Statement._TrieNode()
        for cand in candidates:
            toks = [t.lower() for t in cand.split()]
            node = root
            for tok in toks:
                if tok not in node.children:
                    node.children[tok] = Statement._TrieNode()
                node = node.children[tok]
            # store the original candidate string so we can return it (preserves spacing/casing)
            node.value = cand
        return root

    def _trie_longest_match(self, root: "_TrieNode", tokens: list[str], start: int) -> Optional[Tuple[str, int]]:
        """
        Walk the trie from tokens[start] and return the longest matching candidate:
        (candidate_string, matched_token_count) or None if no match.
        """
        node = root
        best: Optional[Tuple[str, int]] = None
        idx = start
        length = 0
        while idx < len(tokens):
            tok = tokens[idx].lower()
            if tok not in node.children:
                break
            node = node.children[tok]
            length += 1
            idx += 1
            if node.value is not None:
                # record as potential best; continue to prefer longer matches
                best = (node.value, length)
        return best

    def identify_objects(self, candidates: list[str]) -> Tuple[Optional[str], Optional[str], list[str]]:
        """
        Identify up to two objects (primary and secondary after a preposition) using a trie.

        Logic:
          - Work on tokens after the verb (like identify_args).
          - Skip leading separators (articles).
          - Try a longest trie match at the current position to get the primary object.
          - Find the first preposition (if any) after the primary; attempt a secondary match
            after that preposition (skipping articles).
          - Return (primary_candidate_or_None, secondary_candidate_or_None, remaining_tokens).
        """
        original_args = [t for t in self.tokens if t != self.action]
        if not original_args:
            return None, None, []

        trie_root = self._build_trie(candidates)
        removed_indices = set()

        # skip leading separators and mark them removed
        i = 0
        while i < len(original_args) and original_args[i].lower() in SEPARATORS:
            removed_indices.add(i)
            i += 1

        primary: Optional[str] = None
        primary_span: Optional[Tuple[int, int]] = None
        if i < len(original_args):
            match = self._trie_longest_match(trie_root, original_args, i)
            if match:
                primary, plen = match
                primary_span = (i, plen)
                for idx in range(i, i + plen):
                    removed_indices.add(idx)
                i += plen

        # search for first preposition after where we stopped (allow skipping stopwords)
        prep_idx: Optional[int] = None
        search_idx = i
        while search_idx < len(original_args):
            tok = original_args[search_idx].lower()
            if tok in PREPOSITIONS:
                prep_idx = search_idx
                removed_indices.add(prep_idx)
                break
            if tok in SEPARATORS:
                # treat other separators as removable filler
                removed_indices.add(search_idx)
            search_idx += 1

        secondary: Optional[str] = None
        if prep_idx is not None:
            # find start after preposition, skipping separators
            j = prep_idx + 1
            while j < len(original_args) and original_args[j].lower() in SEPARATORS:
                removed_indices.add(j)
                j += 1
            if j < len(original_args):
                sec_match = self._trie_longest_match(trie_root, original_args, j)
                if sec_match:
                    secondary, slen = sec_match
                    for idx in range(j, j + slen):
                        removed_indices.add(idx)

        remaining = [t for idx, t in enumerate(original_args) if idx not in removed_indices]
        return primary, secondary, remaining

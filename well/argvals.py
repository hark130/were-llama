"""Defines the ArgVals data class used by the argument parser to communicate values."""

# Standard
from dataclasses import dataclass, field
# Third Party
# Local


@dataclass
class ArgVals:
    """Return value of the argument parser."""
    use_archive: bool
    debug: bool = field(default=False)

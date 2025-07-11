"""Miscellaneous functionality used by the test framework."""

# Standard Imports
from datetime import datetime
# Third Party Imports
from hobo.subprocess_wrapper import execute_subprocess_cmd
# Local Imports


def get_commit_hash() -> str:
    """Get the top commit hash from git."""
    std_out, std_err = execute_subprocess_cmd(['git', 'rev-parse', 'HEAD'])
    return std_out    


def get_timestamp() -> str:
    """Get the current timestamp of format: YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

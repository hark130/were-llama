#!/bin/bash

# DESCRIPTION:
# This script automates the execution of various checks on the project's code base.  Reviews of
# the test code are a bit more lenient.  All checks will be run, regardless of what is found, but
# this script will exit with a non-zero value if any check fails.
#
# EXIT CODES:
# This script uses the following exit codes:
#   0 on success
#   1 if any command exits with a non-zero value

# GLOBAL VARIABLES
EXIT_CODE=0          # Exit code used by this script
ORIGINAL_DIR=$(pwd)  # Working dir of execution


# CHECK IT
# Pycodestyle
pycodestyle --max-line-length=100 ./
if [ $? -eq 0 ]
then
    echo -e "[✓] Pycodestyle likes the repository"
else
    echo -e "\n\n[X] Pycodestyle does *NOT* like the repository\n"
    EXIT_CODE=1
fi
# Pylint (WERE LLAMA)
find ./well/ -type f -name "*.py" | xargs pylint --score=no
if [ $? -eq 0 ]
then
    echo -e "[✓] Pylint approves of WERE LLAMA"
else
    echo -e "\n\n[X] Pylint does *NOT* approve of WERE LLAMA\n"
    EXIT_CODE=1
fi
# Pylint (Test Code)
find ./test/ -type f -name "*.py" | xargs pylint --score=no --disable=duplicate-code
if [ $? -eq 0 ]
then
    echo -e "[✓] Pylint is happy with the test code"
else
    echo -e "\n\n[X] Pylint is *NOT* happy with the test code\n"
    EXIT_CODE=1
fi


# DONE
cd $ORIGINAL_DIR
echo ""
exit $EXIT_CODE

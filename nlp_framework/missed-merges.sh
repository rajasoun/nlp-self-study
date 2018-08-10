#!/usr/bin/env bash

#usage -> missed_merge to_branch from_branch
#example -> missed_merge master r-1.0.1
#the above script gives all commits that are there on r-1.0.1 that have not been merged with master

if [ $# -lt 2 ]
then
  echo "ERROR: Incorrect Usage"
  echo "Usage: missed_merge.sh <to_branch> <from_branch> [<ignore-commits-file-path>]"
  exit
fi

TO_BRANCH=$1
FROM_BRANCH=$2
IGNORE_COMMITS_FILE="ignored_commits_from_branch_to_master"
if [ $# -gt 2 ]
then
  IGNORE_COMMITS_FILE=$3
fi

echo ">>>> Missed Merges from " $TO_BRANCH..$FROM_BRANCH " <<<"
echo "########################################################"
RAW_UNMERGED_COMMITS=$(git log --oneline $TO_BRANCH..$FROM_BRANCH);
IGNORED_COMMITS=""

IFS=$'\n'

if [ -f $IGNORE_COMMITS_FILE ]; then
  IGNORED_COMMITS=$(cat $IGNORE_COMMITS_FILE);
fi

UNMERGED_COMMIT_COUNT=0

for UNMERGED_COMMIT in $RAW_UNMERGED_COMMITS
do
  COMMIT_MESSAGE=$(echo "$UNMERGED_COMMIT" | sed -e 's/^ *//g' -e 's/ *$//g')
  UNMERGED_COMMIT_MESSAGE=$(echo "$UNMERGED_COMMIT" | cut -d' ' -f2 | sed -e 's/^ *//g' -e 's/ *$//g')
  MATCHED=false;
  for IGNORED_COMMIT in $IGNORED_COMMITS
  do
        case "$COMMIT_MESSAGE" in
      *"$IGNORED_COMMIT"* ) MATCHED=true;break;;
    esac
  done
  if !($MATCHED)
  then
    ESCAPED_COMMIT_MESSAGE=$(printf "%q" $UNMERGED_COMMIT_MESSAGE)
    COMMIT_FOUND_IN_TO_BRANCH=$(git log $TO_BRANCH --oneline | cut -d' ' -f2 | grep $ESCAPED_COMMIT_MESSAGE)
    if test "$COMMIT_FOUND_IN_TO_BRANCH" = ""
    then
      UNMERGED_COMMIT_COUNT=$((UNMERGED_COMMIT_COUNT+1));
      echo "$UNMERGED_COMMIT"
    fi
  fi
done
echo "########################################################"
echo "Found " $UNMERGED_COMMIT_COUNT "missed merges"
exit $UNMERGED_COMMIT_COUNT

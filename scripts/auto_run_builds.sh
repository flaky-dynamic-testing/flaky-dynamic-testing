#!/bin/bash

# Input parameters
REPO_URL=$1
BASE_BRANCH=$2
SHA=$3
GH_TOKEN=$4

# Validate inputs
if [ -z "$REPO_URL" ] || [ -z "$BASE_BRANCH" ] || [ -z "$SHA" ] || [ -z "$GH_TOKEN" ]; then
    echo "Usage: $0 <repo_url> <base_branch> <sha> <gh_token>"
    exit 1
fi

# Extract repo owner and name from URL
REPO_OWNER=$(echo $REPO_URL | cut -d'/' -f4)
REPO_NAME=$(echo $REPO_URL | cut -d'/' -f5)

# Get current timestamp
TIMESTAMP=$(date +%s)

echo "Repo Owner: $REPO_OWNER"
echo "Repo Name: $REPO_NAME"
echo "Base Branch: $BASE_BRANCH"
echo "GH Token: $GH_TOKEN"

BASE_BRANCH_SHA_MSG=$(curl -s -H "Authorization: token $GH_TOKEN" \-H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/git/refs/heads/$BASE_BRANCH)

echo "Base Branch SHA: $BASE_BRANCH_SHA_MSG"
BASE_BRANCH_SHA=$(echo $BASE_BRANCH_SHA_MSG | sed -n 's/.*"sha": "\([^"]*\)".*/\1/p')

# if [ -z "$BASE_BRANCH_SHA" ]; then
#     echo "Failed to get the latest commit SHA of the base branch: $BASE_BRANCH"
#     exit 1
# fi

echo "Base Branch SHA: $BASE_BRANCH_SHA"

if [ -z "$BASE_BRANCH_SHA" ]; then
    echo "Failed to get the latest commit SHA of the base branch: $BASE_BRANCH"
    exit 1
fi

# Create branches and push commits
for i in {1..10}
do
    BRANCH_NAME="${TIMESTAMP}_${i}"
    
    # Create branch from the specified base branch SHA
    curl -s -X POST -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/git/refs \
    -d "{\"ref\":\"refs/heads/$BRANCH_NAME\", \"sha\":\"$BASE_BRANCH_SHA\"}"
    
    # Check if branch creation was successful
    if [ $? -eq 0 ]; then
        echo "Branch created: $BRANCH_NAME"
    else
        echo "Failed to create branch: $BRANCH_NAME"
    fi
done

echo "Repo: $REPO_URL"
echo "Base Branch: $BASE_BRANCH"
echo "SHA: $SHA"
for i in {1..10}
do
    BRANCH_NAME="${TIMESTAMP}_${i}"
    echo "Branch: $BRANCH_NAME"
done

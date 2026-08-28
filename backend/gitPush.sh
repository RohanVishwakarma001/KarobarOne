#!/bin/bash

clear

echo "============================================================"
echo " CREYOTECH GITHUB PUSH UTILITY"
echo "============================================================"
echo ""

echo "Select Developer"
echo "------------------------------------------------------------"
echo "[M] Mousam"
echo "[A] Aditi"
echo "[P] Punit"
echo "[S] Saikat"
echo ""

read -n 1 -p "Press the first letter of your name (M/A/P/S): " CHOICE
echo ""
echo ""

CHOICE=$(echo "$CHOICE" | tr '[:lower:]' '[:upper:]')

case "$CHOICE" in
M)
DEV_NAME="Mousam"
ALLOWED_BRANCH="1-1-bckend-ko"
;;
A)
DEV_NAME="Aditi"
ALLOWED_BRANCH="1-2-bckend-ko"
;;
P)
DEV_NAME="Punit"
ALLOWED_BRANCH="2-1-bckend-ko"
;;
S)
DEV_NAME="Saikat"
ALLOWED_BRANCH="2-2-bckend-ko"
;;
*)
echo ""
echo "❌ Invalid selection."
exit 1
;;
esac

CURRENT_BRANCH=$(git branch --show-current)
REMOTE_URL=$(git config --get remote.origin.url)

echo ""
echo "============================================================"
echo "Repository : $REMOTE_URL"
echo "Developer : $DEV_NAME"
echo "Assigned Branch : $ALLOWED_BRANCH"
echo "Current Branch : $CURRENT_BRANCH"
echo "============================================================"

# -------------------------------------------------------------------
# Verify developer is on the correct branch
# -------------------------------------------------------------------

if [ "$CURRENT_BRANCH" != "$ALLOWED_BRANCH" ]; then
echo ""
echo "❌ ERROR"
echo "------------------------------------------------------------"
echo "You are currently on branch:"
echo " $CURRENT_BRANCH"
echo ""
echo "You are only allowed to push to:"
echo " $ALLOWED_BRANCH"
echo "------------------------------------------------------------"
exit 1
fi

echo ""
echo "✅ Branch verification successful."

# -------------------------------------------------------------------
# Check remote status
# -------------------------------------------------------------------

echo ""
echo "Checking remote branch..."

git fetch origin

if [ $? -ne 0 ]; then
echo ""
echo "❌ Unable to fetch latest changes from GitHub."
exit 1
fi

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$ALLOWED_BRANCH)
BASE=$(git merge-base HEAD origin/$ALLOWED_BRANCH)

if [ "$LOCAL" = "$REMOTE" ]; then

echo "✅ Local branch is up-to-date."

elif [ "$LOCAL" = "$BASE" ]; then

echo ""
echo "============================================================"
echo "❌ YOUR LOCAL BRANCH IS BEHIND THE REMOTE"
echo "============================================================"
echo ""
echo "Please pull the latest changes first."
echo ""
echo "Run:"
echo ""
echo "git pull origin $ALLOWED_BRANCH"
echo ""
exit 1

elif [ "$REMOTE" = "$BASE" ]; then

echo "✅ Local branch contains new commits."

else

echo ""
echo "============================================================"
echo "❌ LOCAL AND REMOTE BRANCH HAVE DIVERGED"
echo "============================================================"
echo ""
echo "Please resolve the conflicts before pushing."
echo ""
echo "Suggested command:"
echo ""
echo "git pull --rebase origin $ALLOWED_BRANCH"
echo ""
exit 1

fi

# -------------------------------------------------------------------
# Show Status
# -------------------------------------------------------------------

echo ""
echo "Current Git Status"
echo "------------------------------------------------------------"

git status

echo "------------------------------------------------------------"
echo ""

# -------------------------------------------------------------------
# Commit Message
# -------------------------------------------------------------------

read -p "Enter Commit Message: " COMMIT_MESSAGE

if [ -z "$COMMIT_MESSAGE" ]; then
echo ""
echo "❌ Commit message cannot be empty."
exit 1
fi

# -------------------------------------------------------------------
# Confirmation before commit
# -------------------------------------------------------------------

echo ""
read -p "Do you want to commit these changes? (Y/N): " COMMIT_CONFIRM

if [[ ! "$COMMIT_CONFIRM" =~ ^[Yy]$ ]]; then
echo ""
echo "Commit cancelled."
exit 0
fi

# -------------------------------------------------------------------
# Add Files
# -------------------------------------------------------------------

echo ""
echo "Adding files..."

git add .

if [ $? -ne 0 ]; then
echo ""
echo "❌ git add failed."
exit 1
fi

# -------------------------------------------------------------------
# Commit
# -------------------------------------------------------------------

echo ""
echo "Creating commit..."

git commit -m "$COMMIT_MESSAGE"

if [ $? -ne 0 ]; then
echo ""
echo "❌ Commit failed."
exit 1
fi

# -------------------------------------------------------------------
# Final Summary
# -------------------------------------------------------------------

echo ""
echo "============================================================"
echo "READY TO PUSH"
echo "============================================================"
echo "Developer : $DEV_NAME"
echo "Repository : $REMOTE_URL"
echo "Target Branch : $ALLOWED_BRANCH"
echo "Commit Message : $COMMIT_MESSAGE"
echo "============================================================"
echo ""

read -p "Do you want to push this commit to '$ALLOWED_BRANCH'? (Y/N): " PUSH_CONFIRM

if [[ ! "$PUSH_CONFIRM" =~ ^[Yy]$ ]]; then
echo ""
echo "Push cancelled."
exit 0
fi

# -------------------------------------------------------------------
# Push
# -------------------------------------------------------------------

echo ""
echo "Pushing code..."
echo ""

git push origin "$ALLOWED_BRANCH"

if [ $? -eq 0 ]; then

echo ""
echo "============================================================"
echo " ✅ PUSH SUCCESSFUL"
echo "============================================================"
echo "Developer : $DEV_NAME"
echo "Branch : $ALLOWED_BRANCH"
echo ""

else

echo ""
echo "============================================================"
echo " ❌ PUSH FAILED"
echo "============================================================"
echo ""
exit 1

fi
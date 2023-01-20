#!/bin/bash

################################################################################################
#
# This script will "merge" the master branch to the "production" branch.
#
# It should be ran only when all the changes are production ready as when it is
# in the production branch, it will be deployed automatically on the Rundeck execution node
#
# @author Arnaud Selvais
#
################################################################################################

# exciting on exception
set -e

ENV_NAME="temporary"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

#
# Simple logging system
#
_log()
{
    LVL="DEBUG"
    if [ $# == 2 ]; then
        LVL=$2
    fi
    echo -e "${GREEN}`date`${NC} - ${BLUE}$LVL${NC} - $1"
}

#
# Checks number or arduments and display documentation
#
if [ "$#" -ne 2 ]; then
    _log "Number of arguments not correct" "ERROR"

    echo "
    Error: $# args, 2 required.

    Documentation:
        Merges master (dev) branch to production, builds zip env and push to GIT

    Usage:
        $0 buildzip release
    
    Example:
        $0 release \"\"       # Will do the release without building the zip end
        $0 \"\" buildzip      # Will only build the zip without releasing to prod
        $0 release buildzip # Will do both

    " >&2
  exit 1
fi

#
# Build the portable environment and zip it
#
build_env_zip()
{
    _log "Building environment in zip file ..."
    _log "Cleaning conda env"
    conda clean --all -y
    conda remove -n $ENV_NAME --all -y
    _log "Creating a new conda env"
    conda create -n $ENV_NAME --copy -y -q python=3.6.8
    _log "Activating env"
    source activate $ENV_NAME
    _log "Copying all local python libs to conda env"
    cp -R ~/.local/lib/python3.6/site-packages/* ~/.conda/envs/$ENV_NAME/lib/python3.6/site-packages/
    cd ~/.conda/envs/
    _log "Zipping the whole env"
    zip -r ../../$ENV_NAME.zip $ENV_NAME
    cd ~/
    _log "Deactivating env"
    source deactivate
    _log "Creating checksum file"
    md5sum temporary.zip > temporary.md5
    _log "Building environment in zip file ... DONE ..."
}

#######################################################################################

#
# Build the env zip if "buildzip" param is passed as 2nd arg
#
if [ "$2" == "buildzip" ]; then
    _log "Build zip env"
    build_env_zip
    _log "Add zip file to git"
    git add temporary.zip
    git add temporary.md5
    _log "Commit changes to git"
    git commit -m "zip env added"
    _log "Push zip file to git master branch"
    git push origin master
fi

#
# Merge master (dev) branch to production and push changes
# if 1st param is "release"
#
if [ "$1" == "release" ]; then
    _log "Set to Production branch"
    git checkout production
    _log "update production"
    git pull origin production
    _log "Pull master to production"
    git pull origin master
    _log "Push merged version to remote production"
    git push origin production
    _log "Set the current branch back to master"
    git checkout master
    _log "Finished :-) ..."
fi

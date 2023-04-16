#!/bin/bash

git fetch --all -p; git branch -vv | grep ": gone]" | awk '{ print "git branch -D "$1 }' | sh

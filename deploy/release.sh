#!/bin/bash

RELEASE_TAG_CURRENT=$(git tag -l | tail -1)
RELEASE_TAG_PREVIOUS=$(git tag -l | tail -2 | head -1)

./gitchangelog.py ^${RELEASE_TAG_PREVIOUS}..${RELEASE_TAG_CURRENT}

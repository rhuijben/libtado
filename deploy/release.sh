#!/bin/bash

if [ -z "$1" ] ; then
	echo "Usage: deploy/release.sh <RELEASE_TAG_CURRENT>"
	echo "         RELEASE_TAG_CURRENT: Release Tag lik 3.0.1.dev"
	exit 128
fi

RELEASE_TAG_CURRENT=$1
RELEASE_TAG_PREVIOUS=$(git tag -l | tail -1)

sed -i "s/^\(  version=\).*/\1'${RELEASE_TAG_CURRENT}',/g" setup.py
sed -i 's/^\(unreleased_version_label = \).*/\1"'${RELEASE_TAG_CURRENT}'"/g' .gitchangelog.rc

./gitchangelog.py ^${RELEASE_TAG_PREVIOUS} HEAD > changelogs/CHANGELOG-${RELEASE_TAG_CURRENT}.rst
git tag -a $RELEASE_TAG_CURRENT -F changelogs/CHANGELOG-${RELEASE_TAG_CURRENT}.rst

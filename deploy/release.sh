#!/bin/bash

if [ -z "$1" ] ; then
	echo "Usage: deploy/release.sh <RELEASE_TAG_CURRENT>"
	echo "         RELEASE_TAG_CURRENT: Release Tag like 3.0.1.dev"
	exit 128
fi

RELEASE_TAG_CURRENT=$1
RELEASE_TAG_PREVIOUS=$(git tag -l | tail -1)

sed -i "s/^\(  version=\).*/\1'${RELEASE_TAG_CURRENT}',/g" setup.py

pipenv run gitchangelog ^${RELEASE_TAG_PREVIOUS} HEAD > changelogs/CHANGELOG-${RELEASE_TAG_CURRENT}.rst
git add changelogs/CHANGELOG-${RELEASE_TAG_CURRENT}.rst setup.py
git commit -m 'chore(changelog): Changelog for version '$RELEASE_TAG_CURRENT
git push origin master
git tag -a $RELEASE_TAG_CURRENT -F changelogs/CHANGELOG-${RELEASE_TAG_CURRENT}.rst
git push origin ${RELEASE_TAG_CURRENT}

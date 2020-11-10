#! /usr/bin/bash

NEW_TAG=`date +R%F`
git tag -a ${NEW_TAG} -m ${NEW_TAG} && git push --follow-tags

#!/bin/bash

DEPLOY_BRANCHES=(master develop)

for i in "${DEPLOY_BRANCHES[@]}"; do
    if [[ "$i" = $TRAVIS_BRANCH ]]; then
        ssh -i deploy_key.pem -oStrictHostKeyChecking=no deploy@5.45.110.119 sudo ./deploy_$TRAVIS_BRANCH.sh
        break
    fi
done

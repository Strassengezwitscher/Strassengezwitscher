#!/bin/bash

DEPLOY_BRANCHES=(master develop)

if [[ $TRAVIS_PYTHON_VERSION = "2.7" ]]; then
    for i in "${DEPLOY_BRANCHES[@]}"; do
        if [[ "$i" = $TRAVIS_BRANCH ]]; then
        	openssl aes-256-cbc -K $encrypted_423a58ca66b3_key -iv $encrypted_423a58ca66b3_iv -in deploy_key.pem.enc -out deploy_key.pem -d
			chmod 600 deploy_key.pem
            ssh -i ./deploy_key.pem -oStrictHostKeyChecking=no travis@5.45.110.119 sudo ./deploy_$TRAVIS_BRANCH.sh
            break
        fi
    done
fi

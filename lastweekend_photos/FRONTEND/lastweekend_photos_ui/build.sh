#! /bin/bash

inc_ver_type=patch
if [ -n "$1" ]; then
    inc_ver_type=$1
fi
version=$(npm version ${inc_ver_type})
version=${version:1}
echo "Building version [${version}] ..."
npm run build
git add -A
git commit -a
# git tag ${version}
echo "Built version [${version}] => OK"

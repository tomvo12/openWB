#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_leaf
$OPENWBBASEDIR/modules/soc_leaf/main.sh 2
exit 0

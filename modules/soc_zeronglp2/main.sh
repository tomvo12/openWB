#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_zerong
$OPENWBBASEDIR/modules/soc_zerong/main.sh 2
exit 0

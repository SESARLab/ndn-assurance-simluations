#!/bin/sh
set -e

SAFE_IDENTITY=/root/identity/safe
UNSAFE_IDENTITY=/root/identity/unsafe

NDNSEC_CMD=`which ndnsec`
echo "Using $NDNSEC_CMD"


echo "Generating safe identity and set as default"
$NDNSEC_CMD key-gen -i $SAFE_IDENTITY
echo "Generating unsafe identity"
$NDNSEC_CMD key-gen -i $UNSAFE_IDENTITY -n

function clean_exit() {
  echo "Removing simulation keys: $SAFE_IDENTITY $UNSAFE_IDENTITY"
  $NDNSEC_CMD delete $SAFE_IDENTITY;
  $NDNSEC_CMD delete $UNSAFE_IDENTITY;
  exit 0
}

echo "Signing unsafe identity with safe identity using an invalid time frame"
$NDNSEC_CMD cert-install <( \
	$NDNSEC_CMD cert-gen -S 20200101000000 -E 20210101000000 <( \
		$NDNSEC_CMD sign-req $UNSAFE_IDENTITY) \
	)
echo "Unsafe certificate signed with wrong time interval"

echo "Sleeping for 10 seconds"
sleep 10

echo "Removing invalid identity"
$NDNSEC_CMD delete $UNSAFE_IDENTITY

echo "Sleeping for 10 seconds"
sleep 10

echo "Setting safe identity as default"
$NDNSEC_CMD set-default $SAFE_IDENTITY

echo "Waiting for user to stop the misconfiguration"
trap clean_exit SIGINT
trap clean_exit SIGTSTP

while true; do
  sleep 1;
done

#! /bin/sh

abs_dir() {
  cd "${1%/*}"; link=`readlink ${1##*/}`;
  if [ -z "$link" ]; then pwd; else abs_dir $link; fi
}
ROOT_PATH=`abs_dir ${BASH_SOURCE:-$0}`
cd ${ROOT_PATH}

. ${ROOT_PATH}/deploy-setup

set -e

export LOCAL_DOT_SSH_PATH=${LOCAL_ROOT_DOT_SSH_PATH}
export PUBLIC_KEY="$( cat ${LOCAL_ROOT_DOT_SSH_PATH}/*.pub )"
export REMOTE_HOST_ADDR_FILE="ip_addr"

python -u setup.py

export REMOTE_HOST=`cat ${REMOTE_HOST_ADDR_FILE}`
rm -f ${REMOTE_HOST_ADDR_FILE}

RETRY=0; MAX_RETRY=10
until [ ${RETRY} -ge ${MAX_RETRY} ]; do
  quiet nc -w 10 ${REMOTE_HOST} 22 && break
  RETRY=`expr ${RETRY} + 1`
  echo "Server not accepting SSH connections yet. Retrying... (${RETRY}/${MAX_RETRY})"
  sleep 2
done

[ ${RETRY} -ge ${MAX_RETRY} ] && echo "Failed to connect to server. Try again later." && exit 1

. ${ROOT_PATH}/deploy-run

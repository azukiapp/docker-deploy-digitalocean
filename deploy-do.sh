#! /bin/sh

set -x

if [ -z ${PROJECT_SRC_PATH} ] || [ ! -d ${PROJECT_SRC_PATH} ]; then
  echo "Failed to locate source dir ${PROJECT_SRC_PATH}"
  exit 1
fi

quiet() {
  ( $@ ) > /dev/null 2>&1
}

abs_dir() {
  cd "${1%/*}"; link=`readlink ${1##*/}`;
  if [ -z "$link" ]; then pwd; else abs_dir $link; fi
}
ROOT_PATH=`abs_dir ${BASH_SOURCE:-$0}`
cd ${ROOT_PATH}

set -e

ROOT_SSH_PATH="/root/.ssh"
mkdir -p ${ROOT_SSH_PATH}
if [ -d ${LOCAL_SSH_KEYS_PATH} ] && quiet ls ${LOCAL_SSH_KEYS_PATH}/*.pub; then
  if [ "${LOCAL_SSH_KEYS_PATH%/}" != "${ROOT_SSH_PATH}" ]; then
    cp -R ${LOCAL_SSH_KEYS_PATH}/* ${ROOT_SSH_PATH}
  fi
else
  if ! quiet ls ${ROOT_SSH_PATH}/id_rsa.pub; then
    ssh-keygen -t rsa -b 4096 -N "" -f ${ROOT_SSH_PATH}/id_rsa
  fi
fi
export LOCAL_SSH_KEYS_PATH=${ROOT_SSH_PATH}
export PUBLIC_KEY="$( cat ${ROOT_SSH_PATH}/*.pub )"

export IP_ADDR_FILE="ip_addr"
python setup.py
export ANSIBLE_SSH_HOST=`cat ${IP_ADDR_FILE}`
rm -f ${IP_ADDR_FILE}

RETRY=0; MAX_RETRY=10
until [ ${RETRY} -ge ${MAX_RETRY} ]; do
  quiet nc -w 10 ${ANSIBLE_SSH_HOST} 22 && break
  RETRY=$[${RETRY}+1]
  echo "Server not accepting SSH connections. Retrying... (${RETRY}/${MAX_RETRY})"
  sleep 2
done

[ ${RETRY} -ge ${MAX_RETRY} ] && echo "Failed to connect to server. Try again later." && exit 1

./deploy.sh

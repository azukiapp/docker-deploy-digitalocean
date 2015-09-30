export LOCAL_DOT_SSH_PATH=${LOCAL_ROOT_DOT_SSH_PATH}
# TO BE FIXED!
export PUBLIC_KEY="$( cat ${LOCAL_ROOT_DOT_SSH_PATH}/*.pub )"
export REMOTE_HOST_ADDR_FILE="ip_addr"

python -u setup.py

export REMOTE_HOST=`cat ${REMOTE_HOST_ADDR_FILE}`
rm -f ${REMOTE_HOST_ADDR_FILE}

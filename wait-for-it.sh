#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

TIMEOUT=30
QUIET=0
HOST=""
PORT=""

echoerr() {
  if [ "$QUIET" -ne 1 ]; then echo "$@" 1>&2; fi
}

usage() {
  cat << USAGE >&2
Usage:
  $0 host:port [-t timeout] [-- command args]
  -q | --quiet                        Do not output any status messages
  -t TIMEOUT | --timeout=timeout      Timeout in seconds, zero for no timeout
  -- COMMAND ARGS                     Execute command with args after the test finishes
USAGE
  exit 1
}

wait_for() {
  if [ "$TIMEOUT" -gt 0 ]; then
    echoerr "$0: waiting $TIMEOUT seconds for $HOST:$PORT"
  else
    echoerr "$0: waiting for $HOST:$PORT without a timeout"
  fi
  start_ts=$(date +%s)
  while :
  do
    if [ "$ISBUSY" -eq 1 ]; then
      nc -z $HOST $PORT
      result=$?
    else
      (echo > /dev/tcp/$HOST/$PORT) >/dev/null 2>&1
      result=$?
    fi
    if [ $result -eq 0 ]; then
      end_ts=$(date +%s)
      echoerr "$0: $HOST:$PORT is available after $((end_ts - start_ts)) seconds"
      break
    fi
    sleep 1
  done
  return $result
}

wait_for_wrapper() {
  # In order to support SIGINT during timeout: http://unix.stackexchange.com/a/57692
  if [ "$QUIET" -eq 1]; then
    timeout $TIMEOUT $0 --quiet --child --host=$HOST --port=$PORT --timeout=$TIMEOUT &
  else
    timeout $TIMEOUT $0 --child --host=$HOST --port=$PORT --timeout=$TIMEOUT &
  fi
  PID=$!
  trap "kill -INT -$PID" INT
  wait $PID
  RESULT=$?
  if [ $RESULT -ne 0 ]; then
    echoerr "$0: timeout occurred after waiting $TIMEOUT seconds for $HOST:$PORT"
  fi
  return $RESULT
}

while [ $# -gt 0 ]
do
  case "$1" in
    *:* )
    HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
    PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
    shift 1
    ;;
    -q | --quiet)
    QUIET=1
    shift 1
    ;;
    -t)
    TIMEOUT="$2"
    if [ "$TIMEOUT" = "" ]; then break; fi
    shift 2
    ;;
    --timeout=*)
    TIMEOUT="${1#*=}"
    shift 1
    ;;
    --)
    shift
    break
    ;;
    --help)
    usage
    ;;
    *)
    echoerr "Unknown argument: $1"
    usage
    ;;
  esac
done

if [ "$HOST" = "" -o "$PORT" = "" ]; then
  echoerr "Error: you need to provide a host and port to test."
  usage
fi

for cmd in timeout nc
do
  command -v $cmd >/dev/null 2>&1 || {
    echoerr "Error: $cmd is not installed."
    exit 1
  }
done

ISBUSY=$(timeout --version 2>&1 | grep -q "BusyBox" && echo 1 || echo 0)

if [ "$ISBUSY" -eq 1 ]; then
  TIMEOUT_CMD="timeout -t"
else
  TIMEOUT_CMD="timeout"
fi

if [ $# -gt 0 ]; then
  wait_for_wrapper
  RESULT=$?
  if [ $RESULT -eq 0 ]; then
    exec "$@"
  fi
  exit $RESULT
else
  wait_for_wrapper
  exit $?
fi

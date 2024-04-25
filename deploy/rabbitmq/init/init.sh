#!/bin/sh
#
#
(rabbitmqctl wait --timeout 60 "$RABBITMQ_PID_FILE" ; \
  rabbitmqctl add_user "$RABBITMQ_DEFAULT_USER" "$RABBITMQ_TAG_VERSION" 2>/dev/null ; \
  rabbitmqctl set_user_tags "$RABBITMQ_DEFAULT_USER" administrator) &

add_user_with_virtual_host () {
  USERNAME=$1
  PASSWORD=$2
  VIRTUAL_HOST=$3
  USER_TAG=$4
  ( rabbitmqctl wait --timeout 60 "$RABBITMQ_PID_FILE" ; \
  rabbitmqctl add_user "$USERNAME" "$PASSWORD" 2>/dev/null ; \
  rabbitmqctl add_vhost "$VIRTUAL_HOST" ; \
  rabbitmqctl set_user_tags "$USERNAME" "$USER_TAG"; \
  rabbitmqctl set_permissions -p "$VIRTUAL_HOST" "$USERNAME"  ".*" ".*" ".*" ; \
  echo "*** User '$USERNAME' with password '***' completed. ***" ; \
  echo "*** Log in the WebUI at port 15672 (example: http:/localhost:15672) ***") &
}

add_user_with_virtual_host "$POC_USERNAME" \
  "$POC_PWD" \
  "$POC_VIRTUAL_HOST" "poc_ml"

# $@ is used to pass arguments to the rabbitmq-server command.
# For example if you use it like this: docker run -d rabbitmq arg1 arg2,
# it will be as you run in the container rabbitmq-server arg1 arg2
rabbitmq-server "$@"

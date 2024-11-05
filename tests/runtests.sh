#!/bin/sh

url="http://127.0.0.1:8855"

status() {
    printf "\n=====================================================\n"
    printf "%s\n" "$1"
    printf -- "-----------------------------------------------------\n"
}

# Usage: method '{"key": "value"}' /endpoint
post() {
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "$1" $url$2
}
get() {
    curl -X GET -H "Authorization: Bearer $TOKEN" $url$1
}
put() {
    curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "$1" $url$2
}
delete() {
    curl -X DELETE -H "Authorization: Bearer $TOKEN" $url$1
}

# getting a user without auth should fail and return 401 with Forbidden as the body
status "getting /users"
response=$(curl -X GET $url/v1/users/)
echo "GOT: $response"
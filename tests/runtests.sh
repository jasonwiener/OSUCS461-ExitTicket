#!/bin/sh

url="http://127.0.0.1:8855/v1"

status() {
    printf "\n=====================================================\n"
    printf "%s\n" "$1"
    printf -- "-----------------------------------------------------\n"
}

# Usage: method '{"key": "value"}' /endpoint
post() {
    curl -X 'POST' -H "Content-Type: application/json" -d "$1" $url$2
}
get() {
    curl -X 'GET' \
  $url$1 \
  -H 'accept: application/json'
}
put() {
    curl -X 'PUT' -H "Content-Type: application/json" -d "$1" $url$2
}
delete() {
    curl -X 'DELETE' $url$1
}

# getting all users initially should return none initially, 404
status "getting /users"
response=$(get /users/)
echo "GOT: $response"
# posting a user needs an email, should return the user
# errors should be handled
new='{
    "email": "example@gmail.com",
    "time_created": 0
}'

status "posting /users: $new"
response=$(post "$new" /users/)
echo "GOT: $response"

# get the uid 
uid=0

# put
update='{
    "email": "example@gmail.com",
    "time_created": 0
}'

status "putting update: $uid"
response=$(put "$update" /users/$uid)
echo "GOT: $response"

#  get again
status "getting all"
response=$(get /users/)
echo "GOT: $response"

status "getting: $uid"
response=$(get /users/$uid)
echo "GOT: $response"

# delete
status "deleting: $uid"
response=$(delete /users/$uid)
echo "GOT: $response"
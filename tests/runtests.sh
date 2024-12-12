#!/bin/sh

url=${API_URL:-"http://127.0.0.1:8855/v1"}

status() {
    printf "\n=====================================================\n"
    printf "%s\n" "$1"
    printf -- "-----------------------------------------------------\n"
}

# Usage: method '{"key": "value"}' /endpoint
post() {
    curl -s -w "\nHTTP_CODE:%{http_code}" -X 'POST' -H "Content-Type: application/json" -d "$1" $url$2
}
get() {
    curl -s -w "\nHTTP_CODE:%{http_code}" -X 'GET' $url$1 -H 'accept: application/json'
}
put() {
    curl -s -w "\nHTTP_CODE:%{http_code}" -X 'PUT' -H "Content-Type: application/json" -d "$1" $url$2
}
delete() {
    curl -s -w "\nHTTP_CODE:%{http_code}" -X 'DELETE' $url$1
}

# Example Usage
status "Getting /users"
response=$(get /users/)
http_code=$(echo "$response" | tail -n 1 | sed 's/HTTP_CODE://')
echo "GOT: $(echo "$response" | head -n -1)"
echo "HTTP_CODE: $http_code"

if [ "$http_code" -eq 404 ]; then
    echo "No users found, as expected."
else
    echo "Unexpected response."
fi

new='{
    "email": "example@gmail.com",
    "time_created": 0
}'

status "Posting /users: $new"
response=$(post "$new" /users/)
http_code=$(echo "$response" | tail -n 1 | sed 's/HTTP_CODE://')
user_id=$(echo "$response" | head -n -1 | jq -r '.uuid')
echo "GOT: $(echo "$response" | head -n -1)"
echo "HTTP_CODE: $http_code"

if [ "$http_code" -ne 200 ]; then
    echo "Failed to create user"
    exit 1
fi

status "Updating user: $user_id"
update='{
    "email": "updated_example@gmail.com",
    "time_created": 0
}'
response=$(put "$update" /users/$user_id)
http_code=$(echo "$response" | tail -n 1 | sed 's/HTTP_CODE://')
echo "GOT: $(echo "$response" | head -n -1)"
echo "HTTP_CODE: $http_code"

status "Getting user: $user_id"
response=$(get /users/$user_id)
http_code=$(echo "$response" | tail -n 1 | sed 's/HTTP_CODE://')
echo "GOT: $(echo "$response" | head -n -1)"
echo "HTTP_CODE: $http_code"

status "Deleting user: $user_id"
response=$(delete /users/$user_id)
http_code=$(echo "$response" | tail -n 1 | sed 's/HTTP_CODE://')
echo "GOT: $(echo "$response" | head -n -1)"
echo "HTTP_CODE: $http_code"

#!/bin/bash

sed -i "s/__BACKEND_SERVICE_PORT__/$PORT/" index.html
nginx -g "daemon off;"

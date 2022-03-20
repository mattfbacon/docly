#!/bin/sh

case $1 in
	dev)
		(cd client && npx parcel watch --dist-dir ./client/build ./client/src/index.html) &
		(cd server && python backend.py) &
		echo Running >&2
	;;
	*)
		echo "Actions must be one of: dev" >&2
		exit 1
	;;
esac

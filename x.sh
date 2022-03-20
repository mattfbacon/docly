#!/bin/sh

case $1 in
	dev)
		./x.sh dev-client &
		./x.sh dev-server &
	;;
	dev-client)
		npx parcel watch --dist-dir ./client/build ./client/src/index.html
	;;
	dev-server)
		(cd server && python backend.py)
	;;
	build-client)
		npx parcel build --dist-dir ./client/build ./client/src/index.html
	;;
	*)
		echo "Actions must be one of: dev dev-client dev-server build-client" >&2
		exit 1
	;;
esac

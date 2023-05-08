# Gather Solar Data

Gather solar production and home consumption data from a local Enphase Envoy system 
and log to a SQL database.  


# Environment Variables

	ENPHASE_HOST=envoy.local
	ENPHASE_PORT=80
	SOLARDB_USER=
	SOLARDB_PASS=
	SOLARDB_NAME=
	SOLARDB_TABLE=
	SOLARDB_HOST=192.168.11.10
	SOLARDB_PORT=3306
	TZ=America/Los_Angeles



# Command line
To build:

	docker build -t homesolargather .

`-t` tags the build

To build multi-paltform (from Mac):

	docker buildx build -f Dockerfile-gather --platform linux/amd64,linux/arm64,linux/arm/v7 -t tomunger/homesolargather:0.3.0 --push .

To run:

	docker run -d --env-file localenv-prod.txt --name hsgather tomunger/homesolargather:0.3.0

	


`-it` adds a pseudo terminal so you can see what it is doing.

`--rm` removes the container on exit

`--env-file <file>` reads environment variables from a file

`--name` Names the container


docker run in background

	
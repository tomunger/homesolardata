# Dashboard



See article about [building a dashboard](https://josetheengineer.dev/how-to-build-a-dashboard-for-your-peloton-workout-data-using-dash).  

Uses plotly [dash](https://dash.plotly.com/introduction)

# Similar Projects

Github Peterpickle [home-energy](https://github.com/peterpickle/home-energy)

# Environment variables


    ENPHASE_HOST=192.168.11.11
    ENPHASE_PORT=443
    ENPHASE_USERNAME=x
    ENPHASE_PASSWORD=x
    ENPHASE_GWSERIAL=n

    SOLARDB_USER=solarlogger
    SOLARDB_PASS=x
    SOLARDB_NAME=enphasesolar
    SOLARDB_TABLE=production
    SOLARDB_HOST=192.168.11.10
    SOLARDB_PORT=3306
    TZ=America/Los_Angeles

# Dash

Run with the following commands:

    export PYTHONPATH=lib:dashboard
    python -m gunicorn dash-live-parts:server -b :8050

# Docker

Local build

    docker build -t hsdashboard -f Dockerfile-dashboard:0.4.0 .    

Local run   

    docker run --rm -it -p 8050:8050 --env-file localenv-prod.txt --name hsdashboard hsdashboard

Cross platform build
    
    docker buildx build -f Dockerfile-dashboard --platform linux/amd64,linux/arm64 -t tomunger/hsdashboard:0.4.0 --push . 

Pull an image

    docker pull tomunger/hsdashboard:0.4.0

Run as service

    docker run -d -p 8050:8050  --env-file localenv-prod.txt --name hsdashboard tomunger/hsdashboard:0.4.0

 * `-d` runs in the background
 * `-p` map port 8050 to port 8050
 * `--env-file file` reads environment variables from a file
 * `tag` is whatever I pushed to the hub.

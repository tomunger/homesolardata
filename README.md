# homesolardata

Collect and display data from a home solar system. 

This is a work in progress to collect data from our newly installed Enphase solar system.

# Plan

My immediate plan is to implement two components

 - A data logger that collects frequent data points and writes it to a database.
 - A dashboard that can run on a small computer and will display current data and a graph of recent 

My enphase system reports net energy transfer to the grid and solar production.  From that I calculate 
consumption.  Consumption and production are stored in the database.

## Future Enhancements

 - Collect more data, including weather (temperature, humidity, cloud cover)
 - Generalize data collection so that it may include data on individual in-home energy consumption (heating, range, etc)

# Status

The data logger currently runs as from the command line and writes to mariaDB.  I plan to make this into a docker
container and run it in my Synology system.

The data logger uses known API calls to my local Enphase envoy system.  I need to generalize this to interrogate 
the system and discover what the appropriate data points are. 

I'm looking at using Dash (part of plotly) for the dashboard.

# Development Configuration Notes

## Directory Structure

 * `gather` is an application that collects solar production and consumption and writes to a database.  This can be built into a docker container.
 * `lib` is the library of shared code.
 * `analize` are juypter notebooks that analyze data.
 * `dash` is a `dash` dashboard that displays data.


## Environment setup

See notes on [python development](https://code.visualstudio.com/docs/python/environments) in VS Code.

 * `.env` is read by VS Code to configure PYTHONPATH for Code.
 * `.vscode/settings.json` sets `terminal.integrated.env.osx` to define PYTHONPATH.  

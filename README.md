# UK Google Trends head lice analysis

Data gathering code which supports the analysis [here](https://public.flourish.studio/story/2630542/).

## Python setup

Developed in Visual Studio Code using the [Remote-Containers](https://code.visualstudio.com/docs/devcontainers/containers) extension. 

To start the container, open `docker-compose.yml` and select `Docker: Compose Up`. Then find the `head-lice` container and right-click it, choose `Attach Visual Studio Code`. This will open a new window within the container. The first time you run the container you will need to install the Python extension, and choose the Python interpreter at `/usr/local/bin/python`.

You should then be able to step through the code sections in [the Python notebook](download.py) to produce the datasets.

Key Python libraries used are:

* [Pandas](https://pandas.pydata.org/) - for data manipulation
* [Pytrends](https://pypi.org/project/pytrends/) - for getting Google Trends data

# Covid19 Interactive Map for Provinces/territories of Canada

### Overview
Interactive map showing changes (total cases, recovered and deaths) by administrative divisions.
* [Covid-19 Data](https://health-infobase.canada.ca/covid-19/?stat=num&measure=total#a2) - Updated data from the Canadian Government.
* [Shapefile](https://www.arcgis.com/home/item.html?id=dcbcdf86939548af81efbd2d732336db) - Provincial and territorial boundaries of Canada.


#### Running the sample:
```sh
$ docker-compose up -d
$ docker exec -it xxxxxxxxxxxx bash
$ bokeh serve --show canada_covid19_map.py
```

#### Captures:

| Capture 1     | Capture 2     | Capture 3     |
| ------------- | ------------- | ------------- |
| ![alt-text-1](https://github.com/vicent3rod/covid19-canada-interactive-map/blob/master/captures/1.png) | ![alt-text-2](https://github.com/vicent3rod/covid19-canada-interactive-map/blob/master/captures/2.png) | ![alt-text-3](https://github.com/vicent3rod/covid19-canada-interactive-map/blob/master/captures/3.png) 


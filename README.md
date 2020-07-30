# Covid19 Interactive Map for Provinces and territories of Canada

### Overview
Program to compare the performances of matrix multiplications (N by N) in three different ways: 
* Triple do-loop (Traditional Parallel processing).
* matmul(a,b) function.
* dgemm routine (INTEL MKL). 

* [Intel Fortran Compiler](https://software.intel.com/en-us/fortran-compilers) - Builds high-performance applications with Intel processors.

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


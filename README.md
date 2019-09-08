# README

## Build Project

```shell script
git clone 
cd PscUniverse/
git submodule add https://github.com/kermitt2/grobid.git  # If not done yet 
pipenv install --dev  # or `pip -r requirements.txt` if you don"t use pipenv
pipenv install -e .  # or `pip install -e .` if you don"t use pipenv  
```

## Prepare data

PatStat data are provided in large `.zip` chunks. 
We want:
 
- small chunks (for easier parallel processing) 
- in `.gz` format (for easy streaming through `smart_open`) 

```shell script
cd PscUniverse/
sh prepare_tls214.sh data/path  # Nb: no trailing "/" 
```

Take a :zzz: ... or a :coffee: , that should take 15-20min. 

## Process data

### Grobid + CrossRef API

1. Start Grobid server

```shell script
cd grobid/
./gradlew run
```

Nb: don't forget to fill the `grobid-home/config/grobid.properties` to make sure that your requests to CrossRef API can 
be properly identified. See [here][crossref-mailto] for more details.

[crossref-mailto]:(https://grobid.readthedocs.io/en/latest/Consolidation/)


2. Start processing data

````shell script
python3 bin/ProcessCitations.py data/path
````

#### Disclaimer

Although we use multi threading, don't expect to process very large amounts of data with this method.

Bottlenecks:

    - Grobid supports 10 concurrent engines
    - CrossRef API supports 30 requests per second
    
All in all, you can reasonably expect to process ~4 citations per second, ie 100,000 in 7 hours.
 

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

### Grobid + Biblio-Glutton (on AWS)

0. AWS Set up

- Start EC2
- Update ES policy strategy with IPv4 EC2

1. Start biblio-glutton

```shell script
cd biblio-glutton/lookup/
./gradlew clean build
java -jar build/libs/lookup-service-1.0-SNAPSHOT-onejar.jar server data/config/config.yml
curl localhost:8080/service/data  # Check that the service is running properly
```

2. Start Grobid

````shell script
cd SciCit/grobid/
./gradlew run
curl -X POST -d "citations=Graff, Expert. Opin. Ther. Targets (2002) 6(1): 103-113" localhost:8070/api/processCitation
````

3. Start Processing

```shell script
cd SciCit/
# pipenv install --dev
pipenv shell
python bin/ProcessCitations.py ~/data/small_chunks/

```

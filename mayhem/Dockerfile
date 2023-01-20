FROM fuzzers/atheris:2.0.7-python3.9

ADD . /src
WORKDIR /src
RUN python3 -m pip install nltk
RUN python3 -m pip install -U spacy==2.3.5
RUN python3 -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz
RUN python3 -m nltk.downloader words stopwords
RUN python3 -m pip install .


CMD ["/src/mayhem/fuzz_parser.py"]

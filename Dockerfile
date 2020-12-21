FROM grassrootseconomics:bancor

ARG pip_extra_index_url=https://pip.grassrootseconomics.net:8433

COPY ./python/ ./eth-token-endorser

RUN cd eth-token-endorser && \
	pip install --extra-index-url $pip_extra_index_url .


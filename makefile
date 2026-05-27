grobid-up:
	docker compose up -d

grobid-down:
	docker compose down

install:
	pip install -e ".[histo_num_papers]"
	pip install -e ".[keyword_clustering]"
	pip install -e ".[map_articles]"
	pip install -e ".[citation_network]"
	pip install -e ".[screening]"

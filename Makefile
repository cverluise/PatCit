.PHONY: clean requirements.txt

requirements.txt:
	poetry export -f requirements.txt > requirements.txt

models/:
	# tar <dest-name.tar.gz> <src-folder>  ## used for compression
	curl -o models -LJO  https://github.com/cverluise/PatCit/releases/download/v0.2-npl/en_core_web_sm_npl-class-ensemble-0.8.tar.gz
	tar -xvzf models/en_core_web_sm_npl-class-ensemble-0.8.tar.gz
	curl -o models -LJO  https://github.com/cverluise/PatCit/releases/download/v0.2-npl/en_core_web_sm_npl-class-ensemble-1.0.tar.gz
	tar -xvzf models/en_core_web_sm_npl-class-ensemble-1.0.tar.gz

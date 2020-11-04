.PHONY: clean requirements.txt docs/ models/ requirements-dev.txt

requirements.txt:
	poetry export -f requirements.txt > requirements.txt

requirements-dev.txt:
	poetry export -f requirements.txt --dev > requirements-dev.txt

models/:
	# tar <dest-name.tar.gz> <src-folder>  ## used for compression
	curl -o models -LJO  https://github.com/cverluise/PatCit/releases/download/v0.2-npl/en_core_web_sm_npl-class-ensemble-0.8.tar.gz
	tar -xvzf models/en_core_web_sm_npl-class-ensemble-0.8.tar.gz
	curl -o models -LJO  https://github.com/cverluise/PatCit/releases/download/v0.2-npl/en_core_web_sm_npl-class-ensemble-1.0.tar.gz
	tar -xvzf models/en_core_web_sm_npl-class-ensemble-1.0.tar.gz

docs/:
	cp LICENSE.md docs/license-mit.md
	cp CONTRIBUTING.md docs/contributing.md
	cp CODE_OF_CONDUCT.md docs/code-of-conduct.md
	curl https://raw.githubusercontent.com/idleberg/Creative-Commons-Markdown/master/4.0/by.markdown > docs/license-cc.md

patcit-gs:
	gsutil -u ${billing-project} -m cp "data-release/*-npl*json*" gs://patcit/npl/json/
	gsutil -u ${billing-project} -m cp "data-release/*-npl*csv*" gs://patcit/npl/csv/
	gsutil -u ${billing-project} -m cp "data-release/*UScontextual*json*" gs://patcit/intext/json/
	gsutil -u ${billing-project} -m cp "data-release/*UScontextual*csv*" gs://patcit/intext/csv/
	gsutil -u ${billing-project} -m cp "data-release/README.md" gs://patcit/

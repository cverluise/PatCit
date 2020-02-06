.PHONY: clean requirements.txt

requirements.txt:
	poetry export -f requirements.txt > requirements.txt

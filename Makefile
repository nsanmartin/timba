tests:
	python3 -m unittest discover unit_test

PYSRC := $(shell find timba -name "*.png" -print)
PYSCRIPTS := $(shell find scripts -name "*.png" -print)

tags: $(PYSRC) $(PYSCRIPTS)
	universal-ctags --exclude="@.gitignore" -R .

lint:
	find . \( -path ./venv -o -path ./build \) -prune -o -name "*.py" \
		-exec pylint {} \;

clean:
	find -name "*.pyc" -delete

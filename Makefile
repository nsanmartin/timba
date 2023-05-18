tests:
	python3 -m unittest discover unit_test

PYSRC := $(shell find timba -name "*.png" -print)

tags: $(PYSRC)
	universal-ctags --exclude="@.gitignore" -R .

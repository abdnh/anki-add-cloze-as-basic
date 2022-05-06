.PHONY = all zip install clean

PACKAGE_NAME := add_cloze_as_basic

all: zip

zip: $(PACKAGE_NAME).ankiaddon

$(PACKAGE_NAME).ankiaddon: src/*
	rm -f $@
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )

# Install in test profile
install:
	rm -rf src/__pycache__
	cp -r src/. ankiprofile/addons21/$(PACKAGE_NAME)

clean:
	rm -f $(PACKAGE_NAME).ankiaddon

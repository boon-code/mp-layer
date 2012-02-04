NAME=mpl
SRCS=src/mpl.py src/download.py src/naming.py

ZIPPER= 
EPYDOC=epydoc

all: info

-include userconfig.mk

ifndef EPYDOC_DIR
	EPYDOC_DIR=html/
endif

EPYDOC_ARGS= -v --parse-only --html --no-frames -o $(EPYDOC_DIR)

PACKET=$(NAME).sh
OBJS=$(SRCS:.py=.notabs)

ifdef PRIVATE
	EPYDOC_LINE= $(EPYDOC) $(EPYDOC_ARGS) $(SRCS)
else
	EPYDOC_LINE= $(EPYDOC) $(EPYDOC_ARGS) --no-private $(SRCS)
endif

ifdef ZIPPER
	ZIPPER_LINE= $(ZIPPER) $(SRCS) -o $(PACKET)
else
	ZIPPER_LINE= @echo "you have to create userconfig.mk and define ZIPPER."
endif

.PHONY: clean git-clean expand docu packet info

info:
	@echo "Commands: expand, docu, packet, clean, git-clean"

git-clean: clean
	@find . -name "*~"
	find . -name "*~" -exec rm "{}" ";"
	@find . -name "*.pyc"
	find . -name "*.pyc" -exec rm "{}" ";"
	rm -rf $(EPYDOC_DIR)

%.notabs : %.py
	expand --tabs=4 $< > $@
	cp $@ $<

expand: $(OBJS)

docu:
	$(EPYDOC_LINE)

clean:
	rm -f $(PACKET)
	find ./src/ -name "*.pyc" -exec rm "{}" ";"
	find ./src/ -name "*.notabs" -exec rm "{}" ";"

packet:
	$(ZIPPER_LINE)

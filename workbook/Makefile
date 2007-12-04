# Makefile for the py4science book.

# Dependencies

# Warning: list the .aux *before* the bbl.  It's probably possible to get the
# rules right, but I'm not sure how.
TEXFILES = $(wildcard *.tex)

SKEL_SRC = workbook_skeletons.aux workbook_skeletons.bbl \
workbook_skeletons.tex $(TEXFILES)

SOL_SRC = $(subst _skeletons,_solved,$(SKEL_SRC))

# programs
PDFTEX = pdflatex -file-line-error
FASTPDFTEX = pdflatex -file-line-error -draftmode -halt-on-error

# convenience shorthand for targets
sol: workbook_solved.pdf
skel: workbook_skeletons.pdf
all: sol skel

# actual targets
workbook_solved.pdf: $(SOL_SRC)
	rm -f problems
	ln -sf problems_solved problems
	$(PDFTEX) workbook_solved
	$(PDFTEX) workbook_solved

workbook_skeletons.pdf: $(SKEL_SRC)
	rm -f problems
	ln -sf problems_skel problems
	$(PDFTEX) workbook_skeletons

workbook_skeletons.tex:
	ln -sf main.tex workbook_skeletons.tex

workbook_solved.tex:
	ln -sf main.tex workbook_solved.tex

clean:
	rm -f *~ *.aux *.log *.toc *.out *.bbl *.blg

distclean: clean
	rm -f workbook_solved.pdf workbook_skeletons.pdf

# Basic rules
empty :=
%.bbl : %.aux
	bibtex $(subst .aux,$(empty),$<)
	$(FASTPDFTEX) $(subst .aux,$(empty),$<)

%.aux : %.tex
	$(FASTPDFTEX) $<

# Phony targets
.PHONY: all clean

# Makefile for the py4science book.

# Dependencies

# Warning: list the .aux *before* the bbl.  It's probably possible to get the
# rules right, but I'm not sure how.
TEXFILES = $(wildcard *.tex)

SKEL_SRC = workbook_skeletons.aux workbook_skeletons.bbl \
workbook_skeletons.tex $(TEXFILES)

SOLN_SRC = $(subst _skeletons,_solutions,$(SKEL_SRC))

# programs
PDFTEX = pdflatex -file-line-error
FASTPDFTEX = pdflatex -file-line-error -draftmode -halt-on-error

# convenience shorthand for targets
sol: workbook_solutions.pdf
skel: workbook_skeletons.pdf
all: sol skel

# actual targets
workbook_solutions.pdf: prob_soln $(SOLN_SRC)
	$(PDFTEX) workbook_solutions
	$(PDFTEX) workbook_solutions

workbook_skeletons.pdf: prob_skel $(SKEL_SRC)
	$(PDFTEX) workbook_skeletons

prob_soln:
	rm -f problems
	ln -sf problems_soln problems
	./update_problems.py

prob_skel:
	rm -f problems
	ln -sf problems_skel problems
	./update_problems.py

workbook_skeletons.tex:
	ln -sf main.tex workbook_skeletons.tex

workbook_solutions.tex:
	ln -sf main.tex workbook_solutions.tex

clean:
	rm -f *~ *.aux *.log *.toc *.out *.bbl *.blg *.fmt

distclean: clean
	rm -f workbook_solutions.pdf workbook_skeletons.pdf problems

# Basic rules
empty :=
%.bbl : %.aux
	bibtex $(subst .aux,$(empty),$<)
	$(FASTPDFTEX) $(subst .aux,$(empty),$<)

%.aux : %.tex
	$(FASTPDFTEX) $<

# Phony targets
.PHONY: all clean prob_soln prob_skel sol skel

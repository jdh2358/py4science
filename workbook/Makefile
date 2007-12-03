solved:
	rm -f problems
	ln -s problems_solved problems
	rm -f workbook_solved.tex
	ln -s main.tex workbook_solved.tex
	pdflatex workbook_solved
	bibtex workbook_solved
	pdflatex workbook_solved
	rm -f workbook_solved.tex

skeletons:
	rm -f problems
	ln -s problems_skel problems
	rm -f workbook_skeletons.tex
	ln -s main.tex workbook_skeletons.tex
	pdflatex workbook_skeletons
	rm -f workbook_skeletons.tex

clean:
	rm -f *~ *.aux *.log *.toc *.out
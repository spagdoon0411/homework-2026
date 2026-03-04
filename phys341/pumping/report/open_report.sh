latexmk -pvc -lualatex -interaction=nonstopmode -pdf -pdflatex='lualatex %O -interaction=nonstopmode %S' -view=pdf-viewer='open -a Skim' report.tex


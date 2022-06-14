#!/usr/bin/env bash
mkdir pages
mkdir pages/eka
mkdir pages/eka/homework
mkdir pages/eka/test
mkdir pages/mok

cd src
files=($(ls *.tex))
for file in "${files[@]}"; do
    if [[ "$1" == "draft" ]]; then
        latexmk -pdf -pdflatex='pdflatex -draftmode %O %S && touch %D' -print=pdf -e '$lpr_pdf=q|pdflatex -interaction=batchmode -synctex=1 %R|' -outdir=../pages ./$file
    else
        latexmk -pdf -outdir=../pages ./$file
    fi
    latexmk -c -outdir=../pages ./$file
done

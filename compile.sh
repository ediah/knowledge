cd src
files=($(ls *.tex))
for file in "${files[@]}"; do
    latexmk -pdf -outdir=../pages ./$file
    latexmk -c -outdir=../pages ./$file
done

files=($(ls src))
for file in "${files[@]}"; do
    latexmk -pdf -outdir=./pages ./src/$file
    latexmk -c -outdir=./pages ./src/$file
done

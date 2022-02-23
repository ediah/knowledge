files=($(ls src))
for file in "${files[@]}"; do
    echo ./src/$file
    #latexmk -pdf -outdir=./pages ./src/$file
    #latexmk -c -outdir=./pages ./src/$file
done

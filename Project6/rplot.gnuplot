set xlabel "Step"
set ylabel "<rsq>"

set term png
set output "rplotRandomStep.png"
plot "rsqrdvals.csv" using 1:2 title "R Sqrd w/ random step walk" w l

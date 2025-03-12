set xlabel "Temp (J/Kb)"
set ylabel "Magnetization (z direction)"
set datafile separator ","

set term png
set output "Fig1.png"
plot "data.csv" using 1:2 notitle w p pt 7

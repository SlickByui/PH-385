set xrange [-0.5:0.5]
set yrange [-0.5:0.5]
set zrange [-0.5:0.5]

set xlabel "X"
set ylabel "Y"
set zlabel "Z"

set size square

set term gif animate 
set output "randomStepWalk.gif"

do for [i=1:200]{
    splot "data.csv" using 1:2:3 index i*5 every ::1::2500 title 'Random Walk w/ random step size' w p pt 7 ps 0.25
    pause 0.02
}


set terminal postscript portrait color enhanced "Helvetica" 16
set size 1, 0.5
set out "../imagenes/tiempo2.eps"
set title "Tiempos de pruebas"
set multiplot

set tmarg 0
set bmarg 0
set lmarg 7
set rmarg 3
set size 1, 0.1
set origin 0.0, 0.500
set yrange [0:5]
set label 1 "Tiempo (minutos)" at graph -0.125, graph 0.5 center rotate
set label "A) Procesar una imagen sin agregar al paciente" at graph 0.24, 1.1
unset key
set style data histogram
set style histogram cluster gap 1
set boxwidth 1
plot "tiempo.dat" u 2:xticlabels(1) lc rgb 'red' t 'h'

set tmarg 0
set bmarg 0
set lmarg 7
set rmarg 3
set size 1, 0.1
set origin 0.0, 0.300
set yrange [0:5]
set label 1 "Tiempo (minutos)" at graph -0.125, graph 0.5 center rotate
set label 2 "B) Procesar una imagen y agregar a un X paciente" at graph 0.24, 1.1
unset key
set style data histogram
set style histogram cluster gap 1
set boxwidth 1
unset title
plot "tiempo.dat" u 3:xticlabels(1) lc rgb 'red' t 'h'

set tmarg 0
set bmarg 0
set lmarg 7
set rmarg 3
set size 1, 0.1
set origin 0.0, 0.075
set yrange [0:5]
set label 1 "Tiempo (minutos)" at graph -0.125, graph 0.5 center rotate
unset label 2
set label 3 "C) Agregar un caso a un nuevo paciente" at graph 0.24, 1.1
unset key
set style data histogram
set style histogram cluster gap 1
set boxwidth 1
unset title
plot "tiempo.dat" u 4:xticlabels(1) lc rgb 'red' t 'h'


unset multiplot	


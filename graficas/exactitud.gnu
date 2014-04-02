limiteErrores = 20
archivo = 'exactitud.dat'
tituloX = 'Rango de edades'
tituloY = 'Errores'
tituloG = 'Exactitud'
pruebaUno = 'Procesar una imagen sin agregar al paciente'
pruebaDos = 'Procesar una imagen y agregar a un X paciente'
pruebaTres = 'Agregar un caso a un nuevo paciente'
rutaImagen = "../imagenes/exactitud2.eps"

red = "#080000"; green = "#000800"; blue = "#000008"

set terminal x11
set terminal postscript enhanced
set title tituloG
set xlabel tituloX
set ylabel tituloY
bw = 0.9
set yrange [0:limiteErrores]
set style data histogram
set style histogram cluster gap 1
set style fill solid
set boxwidth bw
set output rutaImagen

plot archivo u 2:xticlabels(1) lc rgb 'red' t pruebaUno,\
		'' u 3:xticlabels(1) lc rgb 'yellow' t pruebaDos,\
		'' u 4:xticlabels(1) lc rgb 'blue' t pruebaTres



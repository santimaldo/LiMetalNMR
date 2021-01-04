Los archivos "SinglePulse_kX.XX" corresponden a la cantidad de señal luego de excitar con un pulso de _k_ veces 180º.

La señal detectada depende de la profundidad en el metal [1], por eso este archivo es una tabla con muchos valores de señal para un mismo valor de _k_.
Tenemos entonces que cada archivo es una tabla de tres columnas:

beta |  real(S)  | imaginario(S)

donde beta, es el campo B_1 normalizado a la superficie. Es decir, el decaimiendo en profundidad (_r_), con logitud caracteristica (skindepth) _d_:

beta = B_1/B_10 = e^{-r/d}

### Referencias
[1] Mehring, M., Kotzur, D., & Kanert, O. (1972). Influence of the skin effect on the bloch decay in metals. physica status solidi (b), 53(1), K25-K28. https://doi.org/10.1002/pssb.2220530150

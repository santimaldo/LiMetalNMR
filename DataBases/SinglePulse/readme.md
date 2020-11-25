Los archivos _"SinglePulse_kX.XX"_ corresponden a la cantidad de señal luego de excitar con un pulso de _k_ veces 180º.

La señal detectada depende de la profundidad en el metal [1], por eso este archivo es una tabla con muchos valores de señal para un mismo valor de _k_.
Tenemos entonces que cada archivo es una tabla de tres columnas:

beta |  real(S)  | imaginario(S)

donde beta, es el campo $$B_1$$ normalizado a la superficie. Es decir, el decaimiendo con logitud caracteristica (skindepth) _d_

beta = $$e^{-r/d}$$

### Referencias
[1] "Influence of the Skin Effect on the Bloch Decay in Metals" M. Mehring, D. Kotzur, O. Kanert. _Basic Solid State Physics_ (1972) https://doi.org/10.1002/pssb.2220530150


# MAP3121 - Métodos Numéricos e Aplicações - Turma 04
# Exercicio Programa 1

# Autores: Felipe Augusto Martins Pascutti - nUSP: 10705551
#          Lucas Fiori Rodrigues Amorim de Oliveira - nUSP: 10770408

import sys
import time
import datetime
import os
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable

def f_1(t, x):
	# Primeira função f pedida no enunciado, aquela que não é necessário colocar no relatório.
	return ((10*x**2)*(x - 1)) - 60*x*t + 20*t

def f_2(t, x):
	# Segunda função f pedida no enunciado, necessário colocar no relatório.
	return ((10*np.cos(10*t))*(x**2)*(1 - x)**2) - ((1 + np.sin(10*t))*(12*(x**2) - 12*(x) + 2))

def u_exata_1(t, x):
	# Solução exata relativa à função f_1.
	return 10*(t)*(x**2)*(x - 1)

def u_exata_2(t, x):
	# Solução exata relativa à função f_2.
	return (1 + np.sin(10*t))*(x**2)*((1 - x)**2)

def function_matrix(xv, tv, func):
	'''
	Essa função vai pegar uma das funções definidas acima e permitir que calculemos a matriz
	solução de forma simples, via numpy sem precisar iterar "manualmente". Fazer por esse método
	fornece um tempo de execução bem mais rápido, conforme fiz o teste.

	Ela recebe como parâmetro um array x e um array t, devolvendo uma matriz f de tamanho N x M,
	em que temos o valor de f calculado para cada par ordenado (x, t).
	'''
	x_1, t_1 = np.meshgrid(tv, xv)

	if func == 1:
		return f_1(x_1, t_1)

	elif func == 2:
		return f_2(x_1, t_1)

	elif func == 3:
		return f_exata_1(x_1, t_1)

	elif func == 4:
		return f_exata_2(x_1, t_1)

def calcula_erro():
	return 

def primeira_tarefa(N, M, func):

	'''
	Essa função corresponde, de fácil inferência, à geração de gráficos da primeira tarefa do EP.
	A ideia é, fornecido um valor de N e um valor de M (a depender do valor de lambda), além da 
	função f, calcular a matriz f, a matriz u por meio da equação (11) e a matriz u_exata. Com as
	matrizes, plotar dois heatmaps, uma para a matriz u e uma para u_exata na mesma janela. Assim,
	podemos comparar visualmente os valores obtidos.
	'''

	T = 1
	dt, dx = T/M, 1/N

	# O cálculo de lambda é meramente para mostrar no gráfico, pois
	# evidentemente já sabíamos lambda antes de rodarmos a função, aifnal
	# usamos para calcular o valor de M.
	lamb = round((dt/dx**2), 2)

	u = np.zeros((N + 1, M + 1)) # Cria a matriz u inicialmente apenas contendo zeros.
	x = np.arange(N + 1)*dx  # Cria o array de pontos da barra.
	t = np.arange(M + 1)*dt  # Cria o array de tempo.

	start_time = time.time()

	f = function_matrix(x, t, func)

	# Aqui, iteramos "manualmente", pois cada valor de u depende de valores anteriores de u.
	for i in range(1, x.shape[0] - 1):
		for j in range(1, t.shape[0]):
			u[i, j] = u[i, j-1] + (dt*(((u[i-1, j-1] - 2*u[i, j-1] + u[i+1, j-1])/(dx)**2) + f[i, j]))

	elapsed_time = time.time() - start_time # Cálculo simples de tempo de execução.

	if func == 1:
		u_exata = function_matrix(x, t, 4)

	if func == 2:
		u[:, 0] = (x**2)*(1 - x)**2 # Condições iniciais de u para f_2, conforme enunciado.
		u_exata = function_matrix(x, t, 3)

	# Daqui pra cima a etapa operacional está completa. O código que segue tem como objetivo
	# plotar os valores em heatmaps.

	levels1 = MaxNLocator(nbins=N).tick_values(u.min(), u.max())

	# pick the desired colormap, sensible levels, and define a normalization
	# instance which takes data values and translates those into levels.
	cmap = plt.get_cmap('jet')
	norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

	fig, (ax0, ax1) = plt.subplots(nrows=2)

	# contours are *point* based plots, so convert our bound into point
	# centers

	x_1, t_1 = np.meshgrid(t, x)

	cf1 = ax0.contourf(x_1,
					  t_1,	
					  u,
					  levels=levels1,
                  	  cmap=cmap)

	fig.colorbar(cf1, ax=ax0)
	ax0.set_title('Evolução da distribuição da temperatura na barra\n T=1, N={}, λ = {}, Tempo de execução: {:.7f} segundos'.format(N, lamb, elapsed_time))

	levels2 = MaxNLocator(nbins=N).tick_values(u_exata.min(), u_exata.max())

	cf2 = ax1.contourf(x_1,
					   t_1,
					   u_exata,
					   levels=levels2,
					   cmap=cmap)
	
	fig.colorbar(cf2, ax=ax1)
	ax1.set_title('Solução exata')

	# adjust spacing between subplots so `ax1` title and `ax0` tick labels
	# don't overlap
	fig.tight_layout()

	plt.show()


def main():

	while True:

		test = int(input("Qual teste você quer rodar? ")) #Números constam no LEIAME.

		if test == 0:
			break

		#f1, lambda 0.5
		elif test == 1:
			primeira_tarefa(10, 200, 1)
		elif test == 2:
			primeira_tarefa(20, 800, 1)
		elif test == 3:
			primeira_tarefa(40, 3200, 1)
		elif test == 4:
			primeira_tarefa(80, 12800, 1)
		elif test == 5:
			primeira_tarefa(160, 51200, 1)
		elif test == 6:
			primeira_tarefa(320, 204800, 1)

		#f1, lambda 0.25
		elif test == 7:
			primeira_tarefa(10, 400, 1)
		elif test == 8:
			primeira_tarefa(20, 1600, 1)
		elif test == 9:
			primeira_tarefa(40, 6400, 1)
		elif test == 10:
			primeira_tarefa(80, 25600, 1)
		elif test == 11:
			primeira_tarefa(160, 102400, 1)
		elif test == 12:
			primeira_tarefa(320, 409600, 1)

		#f1, lambda 0.51
		elif test == 13:
			primeira_tarefa(10, 196, 1)
		elif test == 14:
			primeira_tarefa(20, 784, 1)
		elif test == 15:
			primeira_tarefa(40, 3137, 1)
		elif test == 16:
			primeira_tarefa(80, 12549, 1)
		elif test == 17:
			primeira_tarefa(160, 50196, 1)
		elif test == 18:
			primeira_tarefa(320, 200784, 1)

		#f2, lambda 0.5
		elif test == 19:
			primeira_tarefa(10, 200, 2)
		elif test == 20:
			primeira_tarefa(20, 800, 2)
		elif test == 21:
			primeira_tarefa(40, 3200, 2)
		elif test == 22:
			primeira_tarefa(80, 12800, 2)
		elif test == 23:
			primeira_tarefa(160, 51200, 2)
		elif test == 24:
			primeira_tarefa(320, 204800, 2)

		#f2, lambda 0.25
		elif test == 25:
			primeira_tarefa(10, 400, 2)
		elif test == 26:
			primeira_tarefa(20, 1600, 2)
		elif test == 27:
			primeira_tarefa(40, 6400, 2)
		elif test == 28:
			primeira_tarefa(80, 25600, 2)
		elif test == 29:
			primeira_tarefa(160, 102400, 2)
		elif test == 30:
			primeira_tarefa(320, 409600, 2)

		#f2, lambda 0.51
		elif test == 31:
			primeira_tarefa(10, 196, 2)
		elif test == 32:
			primeira_tarefa(20, 784, 2)
		elif test == 33:
			primeira_tarefa(40, 3137, 2)
		elif test == 34:
			primeira_tarefa(80, 12549, 2)
		elif test == 35:
			primeira_tarefa(160, 50196, 2)
		elif test == 36:
			primeira_tarefa(320, 200784, 2)

if __name__ == "__main__":
	main()
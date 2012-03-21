#!/usr/bin/env python2
from __future__ import division
import numpy as np
from numpy import array
from math import *
from fractions import Fraction
import csv
from collections import namedtuple

class Method(namedtuple("Method", "alphas betas".split())):
	
	@property
	def k(self):
		return len(self.alphas)


# Euler's method.
euler = Method( alphas = array([-1.0])
              , betas  = array([1.0])
              )

# Method given in the coursework.
b = 3/2
method_2 = Method( alphas = array([-1, -(2*b - 3), 2*b - 3])
                 , betas  = array([0, b, b])
                 )


# The system of ODEs to solve.
def calculate_fs(y, t):
	# Various parameters 
	mu = 0.2
	_lambda = 0.3
	eta = 0.1
	beta_0 = 150
	omega = 8
	
	# T is probably a Fraction when passed in.
	t = float(t)
	
	beta_t = beta_0 * (1 + cos(omega * t))
	
	r = array([ [mu - beta_t * y[0,0] * y[2,0]]
	          , [beta_t * y[0,0] * y[2,0] - (y[1,0] / _lambda)]
	          , [y[1,0] / _lambda - y[2,0] / eta]
	          ]
	         )
	return r


def step((ys, fs), h, t, method):
	h = float(h)
	t = float(t)
	
	new_y = array([[h * np.sum(method.betas * f)
	                - np.sum(method.alphas * y)]
	               for y, f in zip(ys, fs)])
	new_f = calculate_fs(new_y, t)
	
	return ( np.hstack((ys[..., 1:], new_y))
	       , np.hstack((fs[..., 1:], new_f))
	       )
	

def solve_ode(initial, h, ts, method):
	t = Fraction()
	i = 0
	
	current = initial
	ys = []
	fs = []
	ts = ts[:]
	
	while ts:
		current_timesteps = [j * h for j in range(i, i+method.k)]
		while ts and ts[0] in current_timesteps:
			ts_idx = [int((ts[0] - t) / h)]
			ys.append(current[0][..., ts_idx])
			fs.append(current[1][..., ts_idx])
			ts.pop(0)
		next_t = current_timesteps[-1] + h
		current = step(current, h, next_t, method)
		
		t += h
		i += 1
	
	return (np.hstack(ys), np.hstack(fs))


def run(initial_y, h, n_steps):
	# Actual initial values.
	initial = (initial_y, calculate_fs(initial_y, 0.0))
	
	# Run 
	ts = [i * h for i in range(method_2.k)]
	initials = solve_ode(initial, h**2, ts, euler)
	ts = [i * h for i in range(n_steps)]
	ys, fs = solve_ode(initials, h, ts, method_2)
	
	return ys

def run_e(initial_y, h, n_steps):
	initial = (initial_y, calculate_fs(initial_y, 0.0))
	ts = [i * h for i in range(n_steps)]
	ys, fs = solve_ode(initial, h, ts, euler)
	return ys

if __name__ == "__main__":
	initial_y = array([[0.15], [0.6], [0.1]])
	c = csv.DictWriter(open("out.csv", "w"),
	                   "method h t y1 y2 y3".split())
	c.writeheader()
	
	for h in [Fraction(1, 10), Fraction(1, 100), Fraction(1, 300)]:
		ys = run(initial_y, h, int(1 / h))
		for (i, (y1, y2, y3)) in enumerate(zip(*ys)):
			c.writerow(dict( h=str(h)
			               , t=float(h * i)
			               , y1=y1
			               , y2=y2
			               , y3=y3
			               , method="2"
			               )
			          )
	
	for h in [Fraction(1, 10) ** 2, Fraction(1, 100) ** 2]:
		ys = run_e(initial_y, h, int(0.3 / h))
		for (i, (y1, y2, y3)) in enumerate(zip(*ys)):
			c.writerow(dict( h=str(h)
			               , t=float(h * i)
			               , y1=y1
			               , y2=y2
			               , y3=y3
			               , method="euler"
			               ))

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
	
	beta_t = beta_0 * (1 + cos(omega * t * pi))
	
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
	"""Solve an system of ODEs for each t in 'ts', starting with initial values
	'initial', a step size of 'h', and using method 'method'.
	"""
	# The previous m values for y and f.
	current = initial
	# The t of the first pair in curent.
	t = Fraction()
	
	ts = sorted(ts)
	
	# The output, one for each ts.
	ys = []
	fs = []
	
	while ts:
		# The t for each item in current.
		current_timesteps = [t + j * h for j in range(method.k)]
		
		while ts and ts[0] in current_timesteps:
			# We've found one; compute it's index and add it to the output.
			ts_idx = int((ts[0] - t) / h)
			ys.append(current[0][..., [ts_idx]])
			fs.append(current[1][..., [ts_idx]])
			ts.pop(0)
		
		# Step
		next_t = current_timesteps[-1] + h
		current = step(current, h, next_t, method)
		
		t += h
	
	return (np.hstack(ys), np.hstack(fs))


def run(initial_y, h, n_steps):
	"""Find some solutions using method2 bootstrapped with euler's method.
	"""
	# Actual initial values.
	initial = (initial_y, calculate_fs(initial_y, 0.0))
	
	# Bootstrap with euler's method.
	ts = [i * h for i in range(method_2.k)]
	initials = solve_ode(initial, h**2, ts, euler)
	
	# Run with method 2.
	ts = [i * h for i in range(n_steps)]
	ys, fs = solve_ode(initials, h, ts, method_2)
	
	return ts, ys, fs

def run_euler(initial_y, h, n_steps):
	"""Find some solutions usin euler's method (for testing).
	"""
	initial = (initial_y, calculate_fs(initial_y, 0.0))
	ts = [i * h for i in range(n_steps)]
	ys, fs = solve_ode(initial, h, ts, euler)
	return ts, ys, fs

if __name__ == "__main__":
	initial_y = array([[0.15], [0.6], [0.1]])
	c = csv.DictWriter(open("out.csv", "w"),
	                   "method h t y1 y2 y3 f1 f2 f3".split())
	c.writeheader()
	
	for h in [Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000)]:
		ts, ys, fs = run(initial_y, h, int(1 / h) + 1)
		for (t, y1, y2, y3, f1, f2, f3) in zip(ts, *(list(ys) + list(fs))):
			c.writerow(dict( h=str(h)
			               , t=float(t)
			               , y1=y1
			               , y2=y2
			               , y3=y3
			               , f1=f1
			               , f2=f2
			               , f3=f3
			               , method="2"
			               )
			          )
	
	for h in [Fraction(1, 10) ** 2, Fraction(1, 100) ** 2]:
		ts, ys, fs = run_euler(initial_y, h, int(0.3 / h))
		for (t, y1, y2, y3, f1, f2, f3) in zip(ts, *(list(ys) + list(fs))):
			c.writerow(dict( h=str(h)
			               , t=float(t)
			               , y1=y1
			               , y2=y2
			               , y3=y3
			               , f1=f1
			               , f2=f2
			               , f3=f3
			               , method="euler"
			               ))

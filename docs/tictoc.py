#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#  -*- cerebnismus -*-
 
# when you want to calculate run time of a function
# you can use this snippet

import time

def tictoc(func):
		def wrapper(*args, **kwargs):
				start = time.time()
				result = func(*args, **kwargs)
				func_name = func.__name__
				func_args = args
				func_kwargs = kwargs
				print("\n\tfunc: %s(%s)" % (func_name, func_args), " ~ {:.3f} ms \n".format((time.time() - start) * 1000))
				return result
		return wrapper

# usage
# @tictoc
# def func():
#     pass

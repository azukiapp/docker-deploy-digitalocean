# -*- coding: utf-8 -*-

def green(msg):
  return '\033[92m' + msg + '\033[0m'

def red(msg):
  return '\033[91m' + msg + '\033[0m'

def yellow(msg):
  return '\033[93m' + msg + '\033[0m'

def err(msg, tag='ERROR'):
  return red('[' + str(tag).upper() + ']') + ' ' + msg

def warn(msg, tag='WARNING'):
  return yellow('[' + str(tag).upper() + ']') + ' ' + msg

def step(msg):
  print msg,

def step_done():
  print(green('✓'))

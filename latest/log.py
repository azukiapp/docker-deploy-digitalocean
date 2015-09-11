# -*- coding: utf-8 -*-

def red(msg):
  return '\033[91m' + msg + '\033[0m'

def green(msg):
  return '\033[92m' + msg + '\033[0m'

def yellow(msg):
  return '\033[93m' + msg + '\033[0m'

def blue(msg):
  return '\033[94m' + msg + '\033[0m'

def err(msg, tag='ERROR', inline=False):
  if inline:
    print red('[' + str(tag).upper() + ']') + ' ' + msg,
  else:
    print red('[' + str(tag).upper() + ']') + ' ' + msg

def warn(msg, tag='WARNING', inline=False):
  if inline:
    print yellow('[' + str(tag).upper() + ']') + ' ' + msg,
  else:
    print yellow('[' + str(tag).upper() + ']') + ' ' + msg

def info(msg, tag='INFO', inline=False):
  if inline:
    print blue('[' + str(tag).upper() + ']') + ' ' + msg,
  else:
    print blue('[' + str(tag).upper() + ']') + ' ' + msg

def step(msg):
  print msg,

def step_done():
  print(green('✓'))

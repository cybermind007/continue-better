"""
Author: Cort Smith
Version: 1.0.0
Description: Continuation but with better organization and no more need
    for complicated continuation scripts. Using this tool allows you to break
    down your config into individual parts while also maintaining the same
    standard circleci config rules everyone is used to.
Contributors: cybermind007
"""

from yaml import safe_load_all, safe_load, dump_all
import os

with open('rules.yml', 'r') as file:
  rules = safe_load(file)
  config = ''
  index = 0
  for keyfilename in rules['files']:
    tlf = './config/{}'.format(keyfilename)
    # Handle for top-level files
    if os.path.isfile(tlf):
      with open(tlf, 'r') as file:
        config += file.buffer.read().decode()
      config += '\n'
    # Handle for top-level directories
    elif os.path.isdir(tlf):
      config += '{}:\n'.format(keyfilename)
      for filename in os.listdir('{}'.format(tlf)):
        sub_file = '{}/{}'.format(tlf, filename)
        with open(sub_file, 'r') as file:
          next(file)
          for line in file:
            config += line
          config += '\n'

  built_config = safe_load_all(config)
  with open('continuation.yml', 'w+') as file:
    dump_all(built_config, file)

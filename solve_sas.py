#!/usr/bin/env python

from __future__ import print_function

from misc.profiling import *
from misc.utils import SEPARATOR, randomize
from sas.utils import *
from sas.pop import pop_solve
from sas.relaxed_pop import relaxed_pop
from planner.meta.forward_hierarchy import fixed_search, pp_hierarchy_level
import sas.domains as domains
import sys
import getopt
import time
import datetime
import argparse

DIRECTORY = './simulations/sas/planning/'

def solve(problem, print_profile):
  initial, goal, operators = problem()
  dt = datetime.datetime.now()
  directory = DIRECTORY + '{}/{}/{}/'.format(
      problem.__name__, dt.strftime('%Y-%m-%d'), dt.strftime('%H-%M-%S'))
  print(SEPARATOR + '\nSolving sas problem ' + problem.__name__)

  def execute():
    start_time = time.time()
    try:
      output = default_plan(initial, goal, randomize(operators))
      #output = downward_plan(initial, goal, randomize(operators))
      #output = fixed_search(initial, goal, operators, default_plan, pp_hierarchy_level)
      #output = pop_solve(initial, goal, randomize(operators), max_length=2)
      #output = relaxed_pop(initial, goal, operators)
      #output = pop_solve(initial, goal, operators, max_length=6)
      #output = pop_solve(initial, goal, randomize(operators))
    except KeyboardInterrupt:
      output = None, time.time() - start_time
    #make_dir(directory)
    #print('Created directory:', directory)
    return output

  #(plan, state_space), profile_output = profile(execute, filename=directory+'profile')
  (plan, state_space), profile_output = run_profile(execute)
  print('Wrote', directory+'profile')
  print(SEPARATOR)

  data = (str(plan) if plan is not None else 'Infeasible') + '\n\n' + str(state_space)
  print(data)
  #write(directory + 'planner_statistics', data)
  #print('Wrote', directory+'planner_statistics')

  if print_profile:
    print(SEPARATOR)
    print(str_profile(profile_output))
  print(SEPARATOR)

###########################################################################

HELP_MESSAGE = 'python %s -p <problem>'%(__file__)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--problem', default='restack_blocks')
  parser.add_argument('-q', '--profile', action='store_true')
  args = parser.parse_args()

  if hasattr(domains, args.problem):
    problem = getattr(domains, args.problem)
  else:
    print(args.problem, 'is not a valid problem')
    return
  solve(problem, args.profile)

if __name__ == '__main__':
  main()

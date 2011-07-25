#!/usr/bin/env python
"""
User script for importing Pivotal Tracker stories as Lists
and tasks as Tasks in The Hit List

Requires: pivotal-py wrapper: https://github.com/robhudson/pivotal-py
pivotal-py is a *very* lite wrapper around the pivotal api. You'll need
to parse the xml response yourself.

Recommend storing your Pivotal token in a credentials file from your home
~/.pivotaltoken
or store it in the pivotal_token variable
"""
import sys
from os.path import expanduser

from pivotal.pivotal import Pivotal

import TheHitList
thl = TheHitList.Application()

# Config
pivotal_token = ''
pt_token_file = '~/.pivotal_token'
pt_endpoint = 'http://www.pivotaltracker.com/services/v3/'
# EndConfig

pt_token_path = expanduser(pt_token_file)

try:
    pivotal_token = file(pt_token_path).readlines()[0]
except:
    pass

pv = Pivotal(pivotal_token)

boolmap = {
    'true': True,
    'false': False
}

# Get a list of Project ids and names
projects = {}
project_choices = []

_projects = pv.projects().get_etree().findall('project')
for pos, project in enumerate(_projects):
    pid = project.find('id').text
    pname = project.find('name').text
    use_https = boolmap[project.find('use_https').text]
    labels = project.find('labels').text.split(',')
    projects[pos+1] = {
        'id': pid,
        'name': pname,
        'use_https': use_https,
        'labels': labels
        }
    project_choices.append('[%d] %s' % (pos+1, pname))

project_choices.append('[Q(uit)] to Quit')

print "Import Pivotal Tracker stories that have not yet begun into The Hit List"
choice = ''

valid_choices = [str(i) for i in projects.keys() + ['q','Q']]

while choice not in valid_choices:
    print '\n'.join(project_choices)
    choice = raw_input('Choose a Project #: ')

if choice in ['q', 'Q']:
    sys.exit()

project = projects[int(choice)]
if project['use_https']:
    print "This project requires SSL API access, but pivotal-py does not yet support SSL."
    sys.exit(1)

ptlist =  thl.find_list('PT: %s' % (project['name'],))
if not ptlist:
    ptlist = thl.new_list('PT: %s' % (project['name'],))

_stories = pv.projects(project['id']).stories(filter='state:unstarted').get_etree()
for story in _stories:
    newtask = TheHitList.Task()
    newtask.title = story.find('name').text
    newtask.notes = story.find('description').text
    ptlist.add_task(newtask)


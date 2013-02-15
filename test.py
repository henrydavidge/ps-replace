#! /usr/bin/env python

import commands as cmd
import sys
import time

port = sys.argv[1]
fname = sys.argv[2]
rates = []

numbufs = 16

while numbufs <= 240:
	#start server
	for i in range(3):
		cmd.getstatusoutput('pgsql/bin/pg_ctl start -D ~/pgdata -l pre.log -o \"-B '\
		 + str(numbufs) + ' -N 8 -o \'-te -fm -fh\'\"')

		time.sleep(1);
		#connect
		# print cmd.getstatusoutput('pgsql/bin/psql test -p ' + port)

		pre = cmd.getstatusoutput('pgsql/bin/psql test  -p' + port + ' -c \"SELECT blks_read,blks_hit\
		 FROM pg_stat_database WHERE datname=\'test\';\"')
		time.sleep(1)

		cmd.getstatusoutput('pgsql/bin/psql test -p' + port + ' -c \"SELECT * FROM raw_r_tuples;\" > tuples')
		time.sleep(2)

		cmd.getstatusoutput('pgsql/bin/psql test -p' + port + ' -c \"SELECT * FROM raw_r_tuples r, raw_s_tuples s WHERE r.pkey = s.pkey;\" > tuples')
		time.sleep(1)

		post = cmd.getstatusoutput('pgsql/bin/psql test -p' + port + ' -c "SELECT blks_read,blks_hit\
		 FROM pg_stat_database WHERE datname=\'test\';\"')

		post

		pre = [int(s) for s in pre[1].split() if s.isdigit()]
		post = [int(s) for s in post[1].split() if s.isdigit()]
		hr = float((post[1] - pre[1])) / (post[1] - pre[1] + post[0] - pre[0])
		print "Hit Rate: ", hr
		rates.append(str(hr))
		cmd.getstatusoutput('~/pgsql/bin/pg_ctl -D ~/pgdata -l pre.log stop')
		time.sleep(1)
	numbufs += 16

f = open(fname, 'w')
f.write(' '.join(rates))
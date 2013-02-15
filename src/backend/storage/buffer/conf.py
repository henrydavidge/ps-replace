#!/usr/bin/env python

import os, sys, commands

if len(sys.argv) != 2:
	print "Need 2 args"
else:
	commands.getstatusoutput("cp -f bufmgr_" + sys.argv[1] + ".c bufmgr.c")
	commands.getstatusoutput("cp -f freelist_" + sys.argv[1] + ".c freelist.c")
	# if sys.argv[1] == "orig":
	# 	commands.getstatusoutput("cp -f buf_init_orig.c buf_init.c")
	# else:
	# 	commands.getstatusoutput("cp -f buf_init_mod.c buf_init.c")
	os.chdir("/home/accts/hd96/postgresql-9.2.2/")
	os.system("make")
	os.system("make install")
	os.chdir("../")
	commands.getstatusoutput("pgsql/bin/initdb -D pgdata")
	# commands.getstatusoutput("rm pgdata/postgresql.conf")
	# print commands.getstatusoutput("cp /home/accts/hd96/postgresql-9.2.2/src/backend/storage/buffer/postgresql.conf /home/accts/hd96/cs438/pgdata/postgresql.conf")

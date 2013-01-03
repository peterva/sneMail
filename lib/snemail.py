#!/usr/bin/python

import MySQLdb as sql
import sys

conn = None
conf_server ='127.0.0.1'
conf_user = 'mail_test'
conf_pass = 'password'
conf_db = 'mail_test'

def usage():
	print '\n snemail usage examples and conventions:\n'
	print 'snemail list all											- will list all domains, forwardings, transports and users. this is the only option that requires just 2 flags.'
	print 'snemail add domain example.org							- will add example.org to the allowed domains in the postfix config'
	print 'snemail remove transport example.org,127.0.0.1:25		- will add a transport to 127.0.0.1:25 for domain example.org. the transport has to be commaseparated without spaces!'
	print 'snemail add user peter@example.org,password,10000		- will add user peter@example.org to the config with password 'password' (will be crypted in db) and quota 100kb'

def domain_list():
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("SELECT * from domains")
		data = cur.fetchall()
		print "The following domains are configured in snemail:"
		print '\t' + "{0:<30s}".format('domain')
		print '\t' + "{0:<30s}".format('='*30)
		for i in data:
			print '\t' + i[0]
		print ''

	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def forwarding_list():
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("SELECT * from forwardings")
		data = cur.fetchall()
		print "The following forwardings are configured in snemail:"
		print "Entries starting with @ indicate catch-all forwardings."
		print '\t' + "{0:<30s} {1:<30s}".format('source', 'destination')
		print '\t' + "{0:<30s} {1:<30s}".format('='*30, '='*30)
		for i,j in data:
			print '\t' + "{0:<30s} {1:<30s}".format(i, j)
		print ''

	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)
	
	finally:
		if conn:
			conn.close()

def transport_list():
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("SELECT * from transport")
		data = cur.fetchall()
		print "The following transports are configured in snemail:"
		print "Order is important, postfix will be followed from top to bottom."
		print '\t' + "{0:<30s} {1:<30s}".format('domain', 'transport')
		print '\t' + "{0:<30s} {1:<30s}".format('='*30, '='*30)
		for i,j in data:
			print '\t' + "{0:<30s} {1:<30s}".format(i, j)
		print ''

	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def user_list():
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("SELECT * from users")
		data = cur.fetchall()
		print "The following users are configured in snemail:"
		print "Entries in this list will have a real local mailbox."
		print '\t' + "{0:<30s} {1:<30s} {2:<30}".format('email', 'password(crypted)', 'quota')
		print '\t' + "{0:<30s} {1:<30s} {2:<30}".format('='*30, '='*30, '='*30)
		for i,j,k in data:
			print '\t' + "{0:<30s} {1:<30s} {2}".format(i, j, k)
		print ''
	
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def all_list():
	domain_list()
	forwarding_list()
	transport_list()
	user_list()

def domain_add(input):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""INSERT INTO domains VALUES (%s)""", (input))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Domain " + input[0] + " has been added to the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def domain_remove(input):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""DELETE FROM domains WHERE domain=(%s)""", (input))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1:
			print "Domain " + input[0] + " has been removed from the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def forwarding_add(input):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""INSERT INTO forwardings VALUES (%s,%s)""", (input[0],input[1]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Forwarding from " + input[0] + " to " + input[1] + " has been added to the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def forwarding_remove(input):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""DELETE FROM forwardings WHERE source=(%s) AND destination=(%s)""", (input[0],input[1]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Forwarding from " + input[0] + " to " + input[1] + " has been removed from the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def transport_add(input):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""INSERT INTO transport VALUES (%s,%s)""", (input[0],input[1]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Transport from " + input[0] + " has been set to " + input[1] + " and has been added to the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def transport_remove(input):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""DELETE FROM transport WHERE domain=(%s) AND transport=(%s)""", (input[0],input[1]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Transport for domain " + input[0] + " has been removed from the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def user_add(input):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""INSERT INTO users VALUES (%s,ENCRYPT(%s),%s)""", (input[0],input[1],input[2]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "User " + input[0] + " has been added with password " + input[1] + " and quota: " + input[2]
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def user_remove(input):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""DELETE FROM users WHERE email=(%s)""", (input[0]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "User " + input[0] + " has been removed from the database. Maildir is kept intact and in place."
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

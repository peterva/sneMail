#!/usr/bin/env python

import MySQLdb as sql
import sys
from ConfigParser import SafeConfigParser()

conn = None

parser = ConfigParser.SafeConfigParser()
parser.read('/etc/snemail.conf')
conf_server = parser.get('database', 'server')
conf_user = parser.get('database', 'user')
conf_pass = parser.get('database', 'password')
conf_db = parser.get('database', 'database')

def usage():
	print "snemail usage examples and conventions:"
	print "\t" + "{0:<50s} {1:40s}".format("snemail list all",
		"- list all domains, forwardings, transports and users. this is the only option that requires just 2 flags.")
	print "\t" + "{0:<50s} {1:40s}".format("snemail add domain example.org",
		"- add example.org to the allowed domains in the postfix config.")
	print "\t" + "{0:<52s} {1:40s}".format("",
		"domain can also be a subdomain like sub.example.org")
	print "\t" + "{0:<50s} {1:40s}".format("snemail remove transport example.org,127.0.0.1:25",
		"- add a transport to 127.0.0.1:25 for domain example.org. the transport has to be commaseparated without spaces!")
	print "\t" + "{0:<52s} {1:40s}".format("",
		"read transport(5) for more information about transports in postfix")
	print "\t" + "{0:<50s} {1:40s}".format("snemail add user user@example.org,password,10000",
		"- add user user@example.org to the config with password 'password' and quota 100KB")
	print "\t" + "{0:<52s} {1:40s}".format("",
		"password is only plaintext-visible during addition, password will be crypted in the db.")
	print "\t" + "{0:<52s} {1:40s}".format("",
		"quota is done in bytes, so 10000 will equal to 100KB")

def list_domain():
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

def list_forwarding():
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

def list_transport():
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

def list_user():
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

def list_all():
	list_domain()
	list_forwarding()
	list_transport()
	list_user()

def add_domain(entry):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""INSERT INTO domains VALUES (%s)""", (entry))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Domain " + entry[0] + " has been added to the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def remove_domain(entry):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""DELETE FROM domains WHERE domain=(%s)""", (entry))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1:
			print "Domain " + entry[0] + " has been removed from the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def add_forwarding(entry):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""INSERT INTO forwardings VALUES (%s,%s)""", (entry[0],entry[1]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Forwarding from " + entry[0] + " to " + entry[1] + " has been added to the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def remove_forwarding(entry):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""DELETE FROM forwardings WHERE source=(%s) AND destination=(%s)""", (entry[0],entry[1]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Forwarding from " + entry[0] + " to " + entry[1] + " has been removed from the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def add_transport(entry):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""INSERT INTO transport VALUES (%s,%s)""", (entry[0],entry[1]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Transport from " + entry[0] + " has been set to " + entry[1] + " and has been added to the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def remove_transport(entry):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""DELETE FROM transport WHERE domain=(%s) AND transport=(%s)""", (entry[0],entry[1]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "Transport for domain " + entry[0] + " has been removed from the database"
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def add_user(entry):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""INSERT INTO users VALUES (%s,ENCRYPT(%s),%s)""", (entry[0],entry[1],entry[2]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "User " + entry[0] + " has been added with password " + entry[1] + " and quota: " + entry[2]
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

def remove_user(entry):
	try:
		conn = sql.connect(conf_server, conf_user, conf_pass, conf_db);
		cur = conn.cursor()
		cur.execute("""DELETE FROM users WHERE email=(%s)""", (entry[0]))
		if cur.rowcount == 0:
			print "No changes have been made to the database"
		elif cur.rowcount == 1: 
			print "User " + entry[0] + " has been removed from the database. Maildir is kept intact and in place."
		else:
			print 'Unexpected number of rows changed: " + cur.rowcount'
	except sql.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
		if conn:
			conn.close()

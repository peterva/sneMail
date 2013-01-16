#!/bin/bash

# This script needs beautifying, pronto

export BASE=`pwd`

cd /tmp
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY*
yum -q -y install wget

echo '[SNEMAIL] :: Enable RPMForge'
rpm --quiet --import http://dag.wieers.com/rpm/packages/RPM-GPG-KEY.dag.txt
wget --quiet http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.2-2.el6.rf.x86_64.rpm
rpm --quiet -ivh rpmforge-release-0.5.2-2.el6.rf.x86_64.rpm

echo '[SNEMAIL] :: Enable EPEL'
rpm --quiet --import https://fedoraproject.org/static/0608B895.txt
wget --quiet http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm --quiet -ivh epel-release-6-8.noarch.rpm
yum -q -y install yum-priorities
rsync --quiet -av $BASE/epel.repo /etc/yum.repos.d/epel.repo

echo '[SNEMAIL] :: Updating YUM repos' 
yum -q -y update

echo '[SNEMAIL] :: Installing dependencies' 
yum -q -y groupinstall 'Development Tools'
yum -q -y install httpd mysql-server php php-mysql php-mbstring rpm-build gcc mysql-devel openssl-devel cyrus-sasl-devel pkgconfig zlib-devel phpMyAdmin pcre-devel openldap-devel postgresql-devel expect libtool-ltdl-devel openldap-servers libtool gdbm-devel pam-devel gamin-devel libidn-devel db4-devel mod_ssl telnet ntp

echo '[SNEMAIL] :: Installing courier-authlib'
yum -q -y install $BASE/courier-authlib*
chkconfig courier-authlib on
/etc/init.d/courier-authlib start

echo '[SNEMAIL] :: Installing courier-imap'
yum -q -y install $BASE/courier-imap*
chkconfig courier-imap on
/etc/init.d/courier-imap start

echo '[SNEMAIL] :: Installing maildrop'
yum -q -y install $BASE/maildrop*

echo '[SNEMAIL] :: Installing Postfix'
echo '[SNEMAIL] :: http://vault.centos.org/6.2/os/Source/SPackages/postfix-2.6.6-2.2.el6_1.src.rpm patched with http://vda.sourceforge.net/VDA/postfix-2.6.5-vda-ng.patch.gz for quota-support'
yum -q -y install $BASE/postfix*
chkconfig postfix

echo '[SNEMAIL] :: Configuring MySQL'
chkconfig mysqld on
/etc/init.d/mysqld start
mysql_secure_installation

echo '[SNEMAIL :: Configuring PHPMyAdmin'
rsync --quiet -av $BASE/phpMyAdmin.conf /etc/httpd/conf.d/phpMyAdmin.conf
chkconfig httpd on
/etc/init.d/httpd start

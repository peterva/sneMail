#!/bin/bash

# This script needs beautifying, pronto

cd /tmp
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY*

echo 'Enable RPMForge'
rpm --quiet --import http://dag.wieers.com/rpm/packages/RPM-GPG-KEY.dag.txt
wget --quiet http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.2-2.el6.rf.x86_64.rpm
rpm --quiet -ivh rpmforge-release-0.5.2-2.el6.rf.x86_64.rpm

echo 'Enable EPEL'
rpm --quiet --import https://fedoraproject.org/static/0608B895.txt
wget --quiet http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm --quiet -ivh epel-release-6-8.noarch.rpm
yum -qy install yum-priorities
rsync --quiet -av epel.repo /etc/yum.repos.d/epel.repo

echo 'Updating YUM repos' 
yum -qy update

echo 'Installing dependencies' 
yum -qy groupinstall 'Development Tools'
yum -qy ntp httpd mysql-server php php-mysql php-mbstring rpm-build gcc mysql-devel openssl-devel cyrus-sasl-devel pkgconfig zlib-devel phpMyAdmin pcre-devel openldap-devel postgresql-devel expect libtool-ltdl-devel openldap-servers libtool gdbm-devel pam-devel gamin-devel libidn-devel db4-devel mod_ssl telnet

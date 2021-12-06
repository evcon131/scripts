#!/bin/sh
 
# unload all modules
module purge
 
# load modules for install the Perl libraries
module load gcc
module load perl
 
# which version of local::lib should be downloaded and installed?
LOCAL_LIB_URL=http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/local-lib-2.000024.tar.gz
 
# where should local::lib be built?
LOCAL_LIB_SRC=/projects/$USER/perl-local-lib-src
 
# where should local::lib and future Perl libraries be installed?
# NOTE: this needs to be run before using the local Perl libraries
export PERL_LOCAL=/projects/$USER/perl_local
 
# install perl local::lib to the location in $PERL_LOCAL
wget $LOCAL_LIB_URL -O local-lib.tar.gz
mkdir $LOCAL_LIB_SRC -p
tar -xvzf local-lib.tar.gz -C $LOCAL_LIB_SRC --strip-components 1
cd $LOCAL_LIB_SRC
perl Makefile.PL --bootstrap=$PERL_LOCAL
make test && make install
 
# set up environment variables for the local Perl library
# NOTE: this also needs to be run before using the local Perl libraries
eval $(perl -I$PERL_LOCAL/lib/perl5 -Mlocal::lib=$PERL_LOCAL)
 
# use cpan to install the Perl libraries in the new local::lib location
perl -MCPAN -Mlocal::lib=$PERL_LOCAL -e 'CPAN::install DB_File'
perl -MCPAN -Mlocal::lib=$PERL_LOCAL -e 'CPAN::install URI::Escape'
perl -MCPAN -Mlocal::lib=$PERL_LOCAL -e 'CPAN::install Set::IntervalTree'
perl -MCPAN -Mlocal::lib=$PERL_LOCAL -e 'CPAN::install Carp::Assert'
perl -MCPAN -Mlocal::lib=$PERL_LOCAL -e 'CPAN::install JSON::XS'
perl -MCPAN -Mlocal::lib=$PERL_LOCAL -e 'CPAN::install PerlIO::gzip'
perl -MCPAN -Mlocal::lib=$PERL_LOCAL -e 'CPAN::install FindBin'


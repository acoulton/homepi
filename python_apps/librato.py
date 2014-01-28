# Send metrics up to librato
# Requires credentials to be kept in environment variables
# The request processing is heavily based on https://github.com/braindump/Dirty-little-helpers/blob/master/pymetrics

###############################################################################
# pymetrics                                                                   #                         
#                                                                             #
# by Lars Herbach                                                             #
# lars@freistil.cz                                                            #
# http://freistil.cz                                                          #
#                                                                             #
#                                                                             #
# MIT License                                                                 #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining       #
# a copy of this software and associated documentation files (the             #
# "Software"), to deal in the Software without restriction, including         #
# without limitation the rights to use, copy, modify, merge, publish,         #
# distribute, sublicense, and/or sell copies of the Software, and to          #
# permit persons to whom the Software is furnished to do so, subject to       #
# the following conditions:                                                   #
#                                                                             #
# The above copyright notice and this permission notice shall be              #
# included in all copies or substantial portions of the Software.             #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,             #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF          #
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                       #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE      #
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION      #
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION       #
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.             #
###############################################################################

import requests
import time
import os

try:
    user = os.environ['LIBRATO_USER']
    api  = os.environ['LIBRATO_API']
except:
    print "Please set LIBRATO_USER and LIBRATO_API environment variables!"
    print ""
    quit(-1)

def send_librato(payload):
    url  = "https://metrics-api.librato.com/v1/metrics"    
    header = {"content-type": "application/x-www-form-urlencoded"}
    r = requests.post(url,
                      auth = requests.auth.HTTPBasicAuth(user, api),
                      headers = header,
                      data = payload)
    
    if r.status_code != 200:
        print "Error :("
        print r.text
        quit(-1)

# !/bin/bash

# 3-Clause BSD License
# 
# Copyright (c) 2009, Boxed Ice <hello@boxedice.com>
# Copyright (c) 2010-2016, Datadog <info@datadoghq.com>
# Copyright (c) 2020-present, Akita Software <info@akitasoftware.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


PORT=5000
HOST="localhost:${PORT}"
USER_1="2b9046ac-6112-11eb-ae07-3e22fb0d93ba"
USER_2="38c15834-6112-11eb-86fb-3e22fb0d93ba"

echo "Get user info"
curl -s ${HOST}/users/${USER_1}
echo ""
curl -s ${HOST}/users/${USER_2}
echo -e "\n"

echo "Create file 1"
F1=$(curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"contents": "Ode to Akita: A poem."}' \
  ${HOST}/users/${USER_1}/files)
FID1=$(echo ${F1} | jq -r .id)
echo -e "$F1\n"

echo "List files"
curl -s ${HOST}/users/${USER_1}/files
echo -e "\n"

echo "Get file 1"
curl -s ${HOST}/users/${USER_1}/files/${FID1}
echo -e "\n"

echo "Create file 2"
F2=$(curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"contents": "Ode to Akita: A poem."}' \
  ${HOST}/users/${USER_1}/files)
FID2=$(echo ${F2} | jq -r .id)
echo -e "$F2\n"

echo "List files"
curl -s ${HOST}/users/${USER_1}/files
echo -e "\n"

# echo "Delete file 1"
# curl -s -X DELETE ${HOST}/users/${USER_1}/files/${FID1}
# echo -e ""
# 
# echo "Delete file 2"
# curl -s -X DELETE ${HOST}/users/${USER_1}/files/${FID2}
# echo -e ""

echo "Try to get missing file"
curl -s ${HOST}/users/${USER_1}/files/${FID1}
echo ""


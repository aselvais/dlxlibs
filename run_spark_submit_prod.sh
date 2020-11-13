#!/bin/sh

#######################################################################################
#
# Script used to run spark submit jobs - and update the code and env if needed.
# This should be ran as the rundeckadmin user only.
#
# Process description:
#  - pull changes from the production branch (and submodules)
#  - Check if the temporary.zip has changed (with checksum)
#  - If there is a change, unzip and re-build the environment
#  - Set env vars and python vars to local venv then kerberos authenticate
#  - Use the spark-defaults.conf located in the same dir as the py script
#  - If none, use the default one located at the root of the project
#  - Run the spark job
#
# @author Arnaud Selvais
#
#######################################################################################

GREEN='\033[0;32m'
RED='\033[0;101m'
BLUE='\033[0;96m'
NC='\033[0m' # No Color

#
# Simple logging system
#
_log()
{
    LVL="DEBUG"
    if [ $# == 2 ]; then LVL=$2; fi
    ERR=${BLUE}${LVL}${NC};
    if [ "${LVL}" == "WARNING" ]; then ERR=${RED}${LVL}${NC}; fi
    if [ "${LVL}" == "ERROR" ]; then ERR=${RED}${LVL}${NC}; fi
    echo -e "${GREEN}`date`${NC} - $ERR - $1"
}

#
# Decode a JSON + base64 encoded string and put
# the key value pairs as local params
#
decode_base64_json_str()
{
    if [ "$1" != "" ]; then
        json=`echo $1 | base64 -d`
        _log "Json string is: ${json}"
        myvars=`echo $json | sed 's/\\\\\//\//g' | sed 's/[{}]//g' | sed 's/,"/\n"/g' | sed 's/:/=/g' | sed 's/"=/=/g' | sed 's/^"//g' | sed 's/ "/ /g'`
        eval $myvars
    fi
}

#
# Checks number or arduments and display documentation
#
if [ "$#" -ne 3 ]; then
    _log "Number of arguments not correct" "ERROR"

    echo "
    Error: $# args, 3 required.

    Documentation:
        Build process and spark submit.
        Note that the params (if any) have to be JSON strings encoded in Base64.
        If you do not need to pass params, just pass an empty string with \"\"

        shell_params: will setup some local vars in the shell script
        python_params: will be passed as is to the python script

    Usage:
        $0 [shell_params] [python_script] [python_params]
    
    Example:
        $0 \"\" codegen/oracle/grrppr04/grrppr04_ord_admin_import_request_detail_routing.py \"\"
        $0 eyJwYXRoIjoiL3NvbWUvcGF0aC9oZXJlIiwiZmlsZV9sZWZ0IjoibGVmdC50eHQiLCJmaWxlX3JpZ2h0IjoicmlnaHQudHh0In0= utils/jsontohive.py \"\"
    " >&2
  exit 1
fi


## Env Script Vars

PROJ_NAME="rundeckexec"
ENV_NAME="temporary"
EXEC_PATH=$(dirname "$0")
REPO_PATH=$EXEC_PATH
#Example: "codegen/oracle/grrppr04/grrppr04_ord_admin_import_request_detail_routing.py"
SHELL_PARAMS=$1
decode_base64_json_str $SHELL_PARAMS
SCRIPT_PATH=$2
PYTHON_PARAMS=$3
RUNDECK_HOME_PATH=${EXEC_PATH}/../..
TMP_FOLDER=${PROJ_NAME}_env

cd $EXEC_PATH;
_log "Running : $SCRIPT_PATH $PYTHON_PARAMS"

#
# Set the static OS env vars
#
set_static_env_vars()
{
    export JAVA_HOME=/usr/java/jdk1.8.0_202-amd64/jre
    export HADOOP_HOME=/opt/cloudera/parcels/CDH-6.3.3-1.cdh6.3.3.p0.1796617/lib/hadoop/lib/native
    export HADOOP_CONF_DIR=/etc/hadoop/conf.cloudera.hdfs
    export YARN_CONF_DIR=/etc/hadoop/conf.cloudera.yarn
    export SPARK_HOME=/opt/cloudera/parcels/CDH-6.3.3-1.cdh6.3.3.p0.1796617/lib/spark
    export PYSPARK_ARCHIVES_PATH=local:/opt/cloudera/parcels/CDH-6.3.3-1.cdh6.3.3.p0.1796617/lib/spark/python/lib/py4j-0.10.7-src.zip,local:/opt/cloudera/parcels/CDH-6.3.3-1.cdh6.3.3.p0.1796617/lib/spark/python/lib/pyspark.zip
    export ARROW_PRE_0_15_IPC_FORMAT=1
    export PYSPARK_PYTHON=./${PROJ_NAME}_env/temporary/bin/python
    # export PATH=/home/rundeckadmin/repository/$1/$2/TEMPORARY/bin:$PATH
}

#
# Create virt env from the zip file
#
create_environment()
{
    _log "Creating environment ..."
    _log "Removing temp env ..."
    rm -Rf $REPO_PATH/$TMP_FOLDER;
    _log "Creating folder for temp env at $REPO_PATH/$TMP_FOLDER ..."
    mkdir -p $REPO_PATH/$TMP_FOLDER;
    _log "Unzipping content to temp env ..."
    unzip $REPO_PATH/temporary.zip -d $REPO_PATH/$TMP_FOLDER/;
    _log "Moving things around ..."
    mv $REPO_PATH/$TMP_FOLDER/temporary/* $REPO_PATH/$TMP_FOLDER/;
    rmdir $REPO_PATH/$TMP_FOLDER/temporary;
    _log "Creating environment ... DONE ..."
}

#
# Run the spark submit
#
run_spark_submit()
{
    _log "Running spark-submit ..."
    set_static_env_vars
    export KEY="HmNbOyaNOHJM61bIWhnml-6EGkCqse-9UT0iCSdjD7U="
    #export PYSPARK_PYTHON=${PROJ_NAME}_env/bin/python
    export PYTHON_PATH=${PROJ_NAME}_env

    cd $REPO_PATH;
    _log "Kerberos auth ...";
    kinit -kt $RUNDECK_HOME_PATH/rundeckadmin.keytab rundeckadmin@DELUXE.COM;

    # Use the spark config file located in the dir of the script if any (or the default at the root of the project)
    _log "Choosing the right spark-defaults.conf file ...";
    SPARK_CONF_NAME="spark-defaults.conf"
    SPARK_DEFAULTS="${REPO_PATH}/${SPARK_CONF_NAME}"
    SCRIPT_DIR=`dirname ${EXEC_PATH}/${SCRIPT_PATH}`
    if test -f "${SCRIPT_DIR}/${SPARK_CONF_NAME}"; then
        SPARK_DEFAULTS=${SCRIPT_DIR}/${SPARK_CONF_NAME}
        _log "Changed default spark config !" "WARNING"
    fi
    _log "Spark config file used: ${SPARK_DEFAULTS}"

    # Run the job
    _log "Exacuting spark-submit ...";
    spark-submit --master yarn \
                --deploy-mode client \
                --properties-file $SPARK_DEFAULTS \
                --py-files $REPO_PATH/temporary.zip \
                $EXEC_PATH/$SCRIPT_PATH $PYTHON_PARAMS;
}


#######################################################################################

#
# Check if there was a change in the remote repo and pull changes
#
CHANGED=1
_log "Checking checksum on old zip"
MD5_OLD=`md5sum temporary.zip`
_log "Pulling changes from production"
git pull origin production | grep -q 'Already up-to-date.' && CHANGED=0
_log "Checking checksum on new zip"
MD5_NEW=`md5sum temporary.zip`
## update submodules
git submodule update --remote

if [ $CHANGED -eq 1 ]; then
    _log "There was a change, we need to re-build the project." "WARNING"
    if [ "$MD5_OLD" == "$MD5_NEW" ]; then 
        _log "ZIP file did not change... we won't rebuild the env"
    else
        _log "The ZIP has changed... rebuilding the env." "WARNING"
        create_environment
    fi
    run_spark_submit
fi

if [ $CHANGED -eq 0 ]; then
    _log "No change... We can just run the job."
    run_spark_submit
fi

import os
import pipes
import subprocess
import logging

def run(command):
    
    logger = logging.getLogger(__name__)
    
    logger.info(command)
    
    # logger.info(os.environ['PATH'])

    process = subprocess.Popen([command], 
        shell=True, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
    
    stdout = process.stdout.readline()
    stderr = process.stderr.readline()
    
    if stdout: logger.info(stdout)
    if stderr: logger.warning(stderr)

def preBuild(site):
    pass
    
    # For scss/sass you need to install sassc: brew install sassc
    # run('find %s -name "*.scss" -not -name "_*" -exec bash -c "sassc \'{}\' > \'{}.css\'" \;' % pipes.quote(site.static_path))
    
    # For coffee script you need to install coffee script: npm install -g coffee-script
    # run('find %s -name "*.coffee" -exec coffee -c {} \;' % pipes.quote(site.static_path))

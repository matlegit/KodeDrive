import json
import os
import platform
import subprocess
import sys
import traceback


def changes(since_list):

  if since_list:

    modified = []

    for i, val in enumerate(since_list):
      
      file_name = val['name']
      parts = file_name.split('.') # type list

      # if not a temporary Syncthing file  
      if not (parts[0] == '' and parts[1] == 'syncthing' or 
              parts[-1] in ('swp', 'tmp')):
        modified.append(file_name)

    if modified:
      for i, val in enumerate(modified):
        print val

      return True

  else:
    print 'No files modified.'
    return False

def get_watchman():

  ###################
  # TODO: Packaging #
  ###################

  system = platform.system()

  # Linux
  if system == "Linux":
    # subprocess.call("git clone https://github.com/facebook/watchman.git", shell = True)
    pass

  # Mac OSX
  elif system == "Darwin":
    # subprocess.call("brew update; brew install watchman", shell = True) 
    # TODO: What if they don't have brew? 
    pass

  # elif system == "Windows":
  #   return SyncthingClient(
  #     platform_adapter.SyncthingWin64()
  #   ) # TODO: Windows

  else:
    raise Exception("%s is not currently supported." % system)

def since(path, tag):

  since_cmd = "watchman since --no-pretty %s n:%s" % (path, tag)
  stdout = subprocess.check_output(since_cmd.split())

  if not stdout:
    raise IOError("Watchman Since failed.")

  output = json.loads(stdout)
 
  return output['files'] # type: list


def trigger(path):
  # *** TODO: How to call direct command? ***  
  trig_cmd = "watchman -- trigger %s pyfiles '*' -- %/strig.sh" % (path, path)
  
  # subprocess.call(trig_cmd + ' > /dev/null', shell = True)
  # stdout = subprocess.check_output(trig_cmd.split())
 
  # if stdout:
  #   call watchman trigger-list <PATH> and confirm
  #   for i, val in enumerate(outout['triggers']):
  #     if val['name'] != device_id:
  #       raise some error
  #
  # else:
  #   raise ValueError("Watchman trigger failed.")
  
  return

def trigger_rm():
  # watchman trigger-del /root triggername
  return

def trigger_ls(path):
  
  trig_list_cmd = "watchman trigger-list %s" % path
  stdout = subprocess.check_output(trig_list_cmd.split())

  if stdout:
    return json.loads(stdout)

  else:
    raise IOError("Watchman trigger-list failed.")

  return

def watch(path):

  path = os.path.abspath(path)
  path = path.rstrip('/')
  watch_cmd = "watchman watch-project %s" % path
  
  # Init watchman
  stdout = subprocess.check_output(watch_cmd.split())
  
  if stdout:
    output = json.loads(stdout)
    
    try:
      if output['watch'] != path:
        raise IOError("Is Watchman watching %s ?" %  path)

    except KeyError:
      raise ValueError("Failed to read stdout json")

    except IOError as e:
      traceback.print_exc(file = sys.stdout)
      sys.exit(0)

  else:
    raise IOError("Watchman watch-project failed.")

  # Remove this in production
  print "Watching %s\n" % path
  return

def watch_rm(path):
  subprocess.call("watchman watch-del %s > /dev/null" % path, shell = True)
  # TODO: for testing, check if stdout all matches files previously wtached
  return

def watch_rm_all():
  subprocess.call("watchman watch-del-all > /dev/null", shell = True)
  # TODO: for testing, check if stdout all matches files previously wtached
  return

def watch_ls():
  
  stdout = subprocess.check_output("watchman watch-list".split())

  if stdout:
    return json.loads(stdout)

  else:
    raise IOError("Failed to get watch list")

def in_watch_list(path, watch_list = None):
 
  found = False
  path = os.path.abspath(path)

  if not watch_list:
    watch_list = watch_ls()

  for i, val in enumerate(watch_list['roots']):
    if val == path:
      found = True
      break

  if found:
    return True 

  return False

def shutdown():
  subprocess.call("watchman shutdown-server", shell = True)
  return

















import json
import platform
import subprocess


def get_watchman():

  system = platform.system()

  # Linux
  if system == "Linux":
    # subprocess.call("git clone https://github.com/facebook/watchman.git", shell = True)
    pass

  # Mac OSX
  elif system == "Darwin":
    # subprocess.call("brew update; brew install watchman", shell = True) 
    # What if they don't have brew? 
    pass

  # elif system == "Windows":
  #   return SyncthingClient(
  #     platform_adapter.SyncthingWin64()
  #   ) # TODO: Windows

  else:
    raise Exception("%s is not currently supported." % system)

def since(path, tag):

  # since_cmd = "watchman since --no-pretty %s n:%s" % (path, tag)
  stdout = subprocess.check_output(since_cmd.split())

  if stdout:
    # check if valid
    print 'Since valid!'

  else:
    raise IOError("Watchman Since failed.")

  output = json.loads(stdout)
  
  if not output['files']:
    return 'No files modifed.' 
 
  # *** Integrate this into cli_syncthing_adapter.py and cli.py ***
  # modified = []
  #
  # for i, val in enumerate(output['files']):
  #   
  #   file_name = val['name']
  #   parts = file_name.split('.') # type list
  #
  #   # if not a temporary Syncthing file  
  #   if not (parts[0] == '' and parts[1] == 'syncthing' or 
  #           parts[-1] in ('swp', 'tmp')):
  #     modified.append(file_name)
  #
  # if modified:
  #   for i, val in enumerate(modified):
  #     print val
  #   
  # # Sync those files
  #   subprocess.call("kdr push %s" % path, shell = True)   
  
  return output['files']


def trigger(path):
  # *** TODO: Needs more testing ***  
  # trig_cmd = "watchman -- trigger %s pyfiles '*' -- %/strig.sh" % (path, path)
  
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

def trigger_ls():
  # watchman trigger-list /root
  return

def watch(path):

  path = path.rstrip('/')
  watch_cmd = "watchman watch-project %s" % path
  
  # Init watchman
  stdout = subprocess.check_output(watch_cmd.split())
  
  if stdout:
    output = json.loads(stdout)
    
    try:
      if output['watch'] != path:
        raise IOError("Watchman failed to watch %s" %  path)

    except:
      # print output
      # print path
      # print output['watch']
      raise IOError("Watchman watch-project failed.")

  else:
    raise IOError("Watchman watch-project failed.")
  
  return

def watch_rm():
  # watchman watch-del /path/to/dir
  return

def watch_rm_all():
  # watchman watch-del-all
  return

def watch_ls():
  
  stdout = subprocess.check_output("watchman watch-list".split())

  if stdout:
    return json.loads(stdout)

  else:
    raise IOError("Failed to get watch list")

def in_watch_list(watch_list):
 
  for i, val in enumerate(output['roots']):
    if val != path:
      raise IOError("Watchman failed to add %s" %  path)

def watchman_shutdown():
  subprocess.call("watchman shutdown-server", shell = True)
  return

















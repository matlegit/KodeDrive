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

def trigger():
  return

def trigger_rm(): 
  return

def trigger_ls():
  return

def watch():
  return

def watch_rm():
  return

def watch_rm_all():
  return

def watch_ls():
  return

def since():
  return





import os
import pywatchman
import subprocess
import json
import stat


class WatchmanFacade():
  
  client = pywatchman.client()

  ### COMMANDS ###

  def get_pid(self):
    return self.client.query("get-pid")

  def shutdown(self):
    self.client.query("shutdown-server")
    return

  def since(self, path, tag):

    path = os.path.abspath(path)
    output = self.client.query("since", "%s" % path, "n:%s" % tag)

    if output:
      return output['files'] # type: list

    else:
      raise IOError("Watchman Since failed.")

    return

  def trigger(self, path):
    
    path = os.path.abspath(path)
    trig_name = "t" # random? or device_id?

    try: 
      with open(".trig.sh", 'w') as f:

        # Production
        # f.write("#!/bin/sh\nkdr push .")

        # Dev
        try:
          f.write("#!/bin/sh \nexec > log-file 2>&1\necho 'Pushing!'\nkdr push .")
        except:
          raise IOError("Writing shell script failed.")

    except:
      raise IOError("Failed to open/write trigger script")

    # Change permission to be executable
    st = os.stat('.trig.sh')
    os.chmod('.trig.sh', st.st_mode | stat.S_IEXEC)

    output = self.client.query("trigger", path, trig_name, "*", "--", os.path.join(path, ".trig.sh"))

    if output:
      return output # just return for production

    else:
      raise ValueError("Watchman trigger failed.")
    
    return

  def trigger_rm(self, path):

    # TODO: test it
    path = os.path.abspath(path)
    self.client.query("trigger-del", path, "t")

    return

  def trigger_ls(self, path):
   
    path = os.path.abspath(path)

    # Note: querying trigger-list doesn't work with pywatchman :(
    # output = self.client.query("trigger-list %s" % path)
    
    cmd = "watchman trigger-list %s" % path
    stdout = subprocess.check_output(cmd.split())

    if stdout:
      output = json.loads(stdout)

    if output:
      return output 

    else:
      raise IOError("Watchman trigger-list failed.")

    return

  def watch(self, path):

    path = os.path.abspath(path)
    path = path.rstrip('/')
    
    output = self.client.query('watch', path)

    if output:
      try:
        if output['watch'] != path:
          raise IOError("Is Watchman watching %s ?" %  path)

      except KeyError:
        raise ValueError("Failed to read output")

    else:
      raise IOError("Watchman watch failed.")

    # Remove this in production
    print "Watching %s\n" % path
    return

  def watch_project(self, path):
    
    path = os.path.abspath(path)
    path = path.rstrip('/')
    
    output = self.client.query('watch-project', path)

    if output:
      try:
        if output['watch'] != path and output['relative_path'] != os.path.basename(path):
          raise IOError("Is Watchman watching %s ?" %  path)

      except KeyError:
        raise ValueError("Failed to read output")

    else:
      raise IOError("Watchman watch failed.")

    # Remove this in production
    print "Watching %s\n" % path
    return

  def watch_rm(self, path):

    path = os.path.abspath(path)
    self.client.query("watch-del", path)

    return

  def watch_rm_all(self):
    self.client.query("watch-del-all")
    return

  def watch_ls(self):
   
    output = self.client.query("watch-list")

    if output: 
      return output

    else:
      raise IOError("Failed to get watch list")

    return

  # Alternate method to trigger, here for reference
  def wait(self, path):

    path = os.path.abspath(path)
    wait_cmd = "watchman-wait -m 0 %s" % path
    subprocess.call("nohup %s < /dev/null > .changes_log 2>&1 &" % wait_cmd,  shell = True)

    return

  ### UTIL ###

  def get_changes_since(self, path=None, tag=None, since_list=None):

    if not since_list:
      since_list = self.since(path, tag)

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
        return modified

    else:
      return None

  def in_trigger_list(self, path=None, trigger_list=None):

    if not trigger_list:
      trigger_list = self.trigger(path)

    for i, val in enumerate(trigger_list['triggers']):
      if val['name'] == 't':
        return True

    return False

  def in_watch_list(self, path, watch_list=None):
   
    path = os.path.abspath(path)

    if not watch_list:
      watch_list = self.watch_ls()

    for i, val in enumerate(watch_list['roots']):
      if val == path or val in path:
        return True

    return False

  # Only use with wait()
  def changes(self):

    with open(".changes_log") as f:

      if len(f) > 0:
        f.truncate()
        return True

      else:
        return False
    
    return









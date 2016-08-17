import os
import pywatchman


class WatchmanFacade():

  client = pywatchman.client()

### COMMANDS ###

  def shutdown(self):
    self.client("shutdown-server")
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
    
    # *** TODO: How to call direct command? ***  
    trig_cmd = "watchman -- trigger %s pyfiles '*' -- %/strig.sh" % (path, path)
    
    # self.client.query() 

    # if output:
    #   call watchman trigger-list <PATH> and confirm
    #   for i, val in enumerate(outout['triggers']):
    #     if val['name'] != device_id:
    #       raise some error
    #
    # else:
    #   raise ValueError("Watchman trigger failed.")
    
    return

  def trigger_rm(self):
    # watchman trigger-del /root triggername
    return

  def trigger_ls(self, path):
    
    output = self.client.query("trigger-list %s" % path)

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
        if output['watch'] != path: # and output['relative_path'] != os.path.basename(path):
          raise IOError("Is Watchman watching %s ?" %  path)

      except KeyError:
        raise ValueError("Failed to read output")

    else:
      raise IOError("Watchman watch failed.")

    # Remove this in production
    print "Watching %s\n" % path
    return

  # def watch_project():
  #   include?

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

### UTIL ###

  def changes(self, since_list):

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
      # Remove print statement in production
      print 'No files modified.'
      return False

  def in_watch_list(self, path, watch_list = None):
   
    found = False
    path = os.path.abspath(path)

    if not watch_list:
      watch_list = watch_ls()

    for i, val in enumerate(watch_list['roots']):
      if val == path or val in path:
        found = True
        break

    if found:
      return True 

    return False











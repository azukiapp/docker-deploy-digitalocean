# -*- coding: utf-8 -*-

import os
import time
import sys
import digitalocean
import log

def env(key, default=None):
  try:
    return os.environ[key]
  except:
    return default

def wait(action, desciption=None, step=2000, timeout=300000):
  if action is None:
    raise RuntimeError(log.err('Cannot wait for an empty action.'))
  if desciption is None:
    desciption = action.type
  start_time = time.time()
  while (time.time() - start_time)*1000 < timeout:
    action.load()
    if action.status == 'completed':
      return
    elif action.status == 'errored':
      raise RuntimeError(log.err(str(desciption)))
    time.sleep(step/1000)
  if (time.time() - start_time)*1000 >= timeout:
    raise RuntimeError(log.err(str(desciption) + ' Timeout (' + str(timeout) + 'ms)', 'timeout'))

def last_action(droplet):
  if droplet is None:
    return None
  actions = droplet.get_actions()
  if actions.__len__() == 0:
    return None
  else:
    return actions[-1]

def wait_droplet_get_active(droplet, step=2000, timeout=900000):
  if droplet is None:
    raise RuntimeError(log.err('Cannot wait for an empty droplet.'))
  start_time = time.time()
  while (time.time() - start_time)*1000 < timeout:
    droplet.load()
    if droplet.status == 'active':
      return
    elif droplet.status == 'new' or droplet.status == 'off' or droplet.status == 'archive':
      time.sleep(step/1000)
      continue
    else:
      raise RuntimeError(log.err('Failed to put droplet ' + str(droplet.name) + ' up. Status: ' + str(droplet.status)))
  if (time.time() - start_time)*1000 >= timeout:
    raise RuntimeError(log.err('Failed to put droplet ' + str(droplet.name) + ' up. Timeout (' + str(timeout) + 'ms).', 'timeout'))

token = env('DEPLOY_API_TOKEN')
if token is None:
  raise EnvironmentError(log.err('Environment variable DEPLOY_API_TOKEN is empty.'))

public_key = env('PUBLIC_KEY')
if public_key is None:
  raise EnvironmentError(log.err('Environment variable PUBLIC_KEY is empty.'))
key_name = env('KEY_NAME', public_key.split()[-1])

ssh_key = digitalocean.SSHKey(token=token).load_by_pub_key(public_key)
if ssh_key is None:
  ssh_key            = digitalocean.SSHKey(token=token)
  ssh_key.name       = key_name
  ssh_key.public_key = public_key
  ssh_key.create()

droplet_name   = env('AZK_MID', 'azk-deploy')
droplet_name   = env('BOX_NAME', droplet_name)

droplet_region = env('BOX_REGION', 'nyc3')
droplet_image  = env('BOX_IMAGE', 'ubuntu-14-04-x64')
droplet_size   = env('BOX_SIZE', '1gb')
droplet_backup = True if env('BOX_BACKUP', 'false') == 'true' else False
droplet_private_networking = True if env('BOX_PRIVATE_NETWORKING', 'false') == 'true' else False

log.step('Logging into DigitalOcean')
manager  = digitalocean.Manager(token=token)
log.step_done()

log.step('Getting existing droplets')
droplets = manager.get_all_droplets()
log.step_done()

droplet = None
for a_droplet in droplets:
  if a_droplet.name == droplet_name:
    droplet = a_droplet
    break

if not droplet is None and (
  droplet.region['slug']     != droplet_region or
  droplet.image['slug']      != droplet_image  or
  droplet.size['slug']       != droplet_size   or
  droplet.backups            != droplet_backup or
  droplet.private_networking != droplet_private_networking
  ):
  log.warn('Droplet config has changed! It will be destroyed and a new one will be created. Are you sure? (y/N) ', inline=True)
  ans = sys.stdin.read(1)
  if str(ans).lower() == 'y':
    log.step('Destroying existing droplet')
    droplet.destroy()
    wait(last_action(droplet), 'Destroying existing droplet.')
    droplet = None
    log.step_done()
  else:
    log.warn('The existing droplet has been preserved.')

if droplet is None:
  log.step('Creating new droplet ' + droplet_name + ' (please be patient)')
  droplet = digitalocean.Droplet(token=token,
    name=droplet_name,
    region=droplet_region,
    image=droplet_image,
    size_slug=droplet_size,
    ssh_keys=[ssh_key.id],
    backups=droplet_backup,
    private_networking=droplet_private_networking)
  droplet.create()
  wait(last_action(droplet), 'Creating droplet.')
  log.step_done()
else:
  log.step('Existing droplet ' + droplet.name + ' will be used.')
  log.step_done()
  try:
    droplet.power_on()
    log.step('Powering on droplet')
    wait(last_action(droplet), 'Powering on droplet.')
    log.step_done()
  except digitalocean.baseapi.DataReadError:
    pass

log.step('Waiting droplet to get active (please be patient)')
wait_droplet_get_active(droplet)
log.step_done()

droplet.load()
ip_addr_file= env('REMOTE_HOST_ADDR_FILE', 'ip_addr')

with open(ip_addr_file, 'w') as f:
  f.write(str(droplet.ip_address))

print('Droplet has been successfully setup')

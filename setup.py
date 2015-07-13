import os
import time
import digitalocean

def env(key, default=None):
  try:
    return os.environ[key]
  except:
    return default

# Usar metodo wait da action
def wait(action, desciption=None, step=2000, timeout=300000):
  if action is None:
    raise RuntimeError("Cannot wait for an empty action.")
  if desciption is None:
    desciption = action.type
  start_time = time.time()
  while (time.time() - start_time)*1000 < timeout:
    action.load()
    print action.type + action.status
    if action.status == 'completed':
      return
    elif action.status == 'errored':
      raise RuntimeError('[FAIL] ' + str(desciption))
    time.sleep(step/1000)
  if (time.time() - start_time)*1000 >= timeout:
    raise RuntimeError('[TIMEOUT] ' + str(desciption) + ' Timeout (' + str(timeout) + 'ms)')

def last_action(droplet):
  if droplet is None:
    return None
  actions = droplet.get_actions()
  if actions.__len__() == 0:
    return None
  else:
    return actions[-1]

def wait_droplet_get_active(droplet, step=2000, timeout=300000):
  if droplet is None:
    raise RuntimeError("Cannot wait for an empty droplet.")
  start_time = time.time()
  while (time.time() - start_time)*1000 < timeout:
    droplet.load()
    if droplet.status == 'active':
      return
    elif droplet.status == 'new' or droplet.status == 'off' or droplet.status == 'archive':
      time.sleep(step/1000)
      continue
    else:
      raise RuntimeError('[FAIL] Failed to put droplet ' + str(droplet.name) + ' up. Status: ' + str(droplet.status))
  if (time.time() - start_time)*1000 >= timeout:
    raise RuntimeError('[TIMEOUT] Failed to put droplet ' + str(droplet.name) + ' up. Timeout (' + str(timeout) + 'ms).')

token = env('API_TOKEN')
if token is None:
  raise EnvironmentError('Environment variable API_TOKEN is empty.')

key_name = env('KEY_NAME', 'azk-deploy')
public_key = env('PUBLIC_KEY')
if public_key is None:
  raise EnvironmentError('Environment variable PUBLIC_KEY is empty.')

ssh_key = digitalocean.SSHKey(token=token).load_by_pub_key(public_key)
if ssh_key is None:
  ssh_key            = digitalocean.SSHKey(token=token)
  ssh_key.name       = key_name
  ssh_key.public_key = public_key
  ssh_key.create()

droplet_name   = 'azk-' + env('AZK_MID', 'deploy')
droplet_region = env('BOX_REGION', 'nyc3')
droplet_image  = env('BOX_IMAGE', 'ubuntu-14-04-x64')
droplet_size   = env('BOX_SIZE', '1gb')

manager  = digitalocean.Manager(token=token)
droplets = manager.get_all_droplets()

droplet = None
for a_droplet in droplets:
  if a_droplet.name == droplet_name:
    droplet = a_droplet
    break

if not droplet is None and (
  droplet.region['slug'] != droplet_region or
  droplet.image['slug']  != droplet_image  or
  droplet.size['slug']   != droplet_size
  ):
  droplet.destroy()
  wait(last_action(droplet), 'Destroying existing droplet.')

if droplet is None:
  droplet = digitalocean.Droplet(token=token,
    name=droplet_name,
    region=droplet_region,
    image=droplet_image,
    size_slug=droplet_size,
    ssh_keys=[ssh_key.id])
  droplet.create()
  wait(last_action(droplet), 'Creating droplet.')
else:
  try:
    droplet.power_on()
    wait(last_action(droplet), 'Powering on droplet.')
  except digitalocean.baseapi.DataReadError:
    pass

wait_droplet_get_active(droplet)

droplet.load()
ip_addr_file= env('REMOTE_HOST_ADDR_FILE', 'ip_addr')

with open(ip_addr_file, 'w') as f:
  f.write(str(droplet.ip_address))

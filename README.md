[azukiapp/deploy-digitalocean](http://images.azk.io/#/deploy-digitalocean)
==================

Base docker image to deploy an app into DigitalOcean using [`azk`](http://azk.io)

Initial Considerations
---
We strongly recommend you to use Ubuntu 14.04 x86-64 in the target server.
Using this image with any other OS in the target server is untested yet and it's potentially broken.

Versions (tags)
---

<versions>
- [`latest, 0.0.2`](https://github.com/azukiapp/docker-deploy-digitalocean/blob/master/latest/Dockerfile)
- [`0.0.1`](https://github.com/azukiapp/docker-deploy-digitalocean/blob/v0.0.1/latest/Dockerfile)
</versions>

Image content:
---

- Ubuntu 14.04 (v0.0.1) or Alpine Linux (v0.0.2 or later)
- [Ansible](http://www.ansible.com)
- [SSHPass](http://sourceforge.net/projects/sshpass/)
- [python-digitalocean](https://github.com/koalalorenzo/python-digitalocean)

### Configuration
The following environment variables are available for configuring the deployment using this image:

- **DEPLOY_API_TOKEN**: User's API token in [DigitalOcean][do-api-token];
- **BOX_NAME** (*optional, default: `$AZK_MID || azk-deploy`*): Droplet name;
- **BOX_REGION** (*optional, default: nyc3*): Region where the droplet is allocated. Check all available regions and their slugs [here](https://developers.digitalocean.com/documentation/v2/#list-all-regions);
- **BOX_IMAGE** (*optional, default: ubuntu-14-04-x64*): Image used in the droplet. Default is Ubuntu 14.04 x86-64 and **we strongly recommend you to use it**. Check all available images and their slugs [here](https://developers.digitalocean.com/documentation/v2/#list-all-distribution-images);
- **BOX_SIZE** (*optional, default: 1gb*): Size of the droplet (involves number of CPUs, amount of memory, storage capacity and data traffic). Check all available droplet sizes and their slugs [here](https://developers.digitalocean.com/documentation/v2/#list-all-sizes);
- **BOX_BACKUP** (*optional, default: false*): If `true`, enables DigitalOcean [built-in backups](https://www.digitalocean.com/help/technical/backup/);
- **BOX_PRIVATE_NETWORKING** (*optional, default: false*): If `true`, enables DigitalOcean [built-in private networking](https://www.digitalocean.com/company/blog/introducing-private-networking/);
- **LOCAL_PROJECT_PATH** (*optional, default: /azk/deploy/src*): Project source code path;
- **LOCAL_DOT_SSH_PATH** (*optional, default: /azk/deploy/.ssh*): Path containing SSH keys. If no path is given, a new SSH public/private key pair will be generated;
- **LOCAL_DOT_CONFIG_PATH** (*optional, default: `/azk/deploy/.config`*): Path to be mapped as a persistent folder on Azkfile.js. Used to cache deploy information;
- **REMOTE_USER** (*optional, default: git*): Username created (or used if it exists) in the remote server to deploy files and run the app;
- **GIT_REF** (*optional, default: master*): Git reference (branch, commit SHA1 or tag) to be deployed;
- **AZK_DOMAIN** (*optional, default: azk.dev.io*): azk domain in the current namespace;
- **HOST_DOMAIN** (*optional*): Domain name which you'll use to access the remote server;
- **AZK_RESTART_COMMAND** (*optional, default: azk restart -R*): command to executed after each git push;
- **REMOTE_PROJECT_PATH_ID** (*optional*): By default, the project will be placed at */home/`REMOTE_USER`/`REMOTE_PROJECT_PATH_ID`* (i.e., `REMOTE_PROJECT_PATH`) in the remote server. If no value is given, a random id will be generated;
- **REMOTE_PROJECT_PATH** (*optional*): The path where the project will be stored in the remote server. If no value is given, it will be */home/`REMOTE_USER`/`REMOTE_PROJECT_PATH_ID`*;
- **RUN_SETUP** (*optional, default: true*): Boolean variable that defines if the remote server setup step should be run;
- **RUN_CONFIGURE** (*optional, default: true*): Boolean variable that defines if the remote server configuration should be run;
- **RUN_DEPLOY** (*optional, default: true*): Boolean variable that defines if the deploy step should be run;
- **DISABLE_ANALYTICS_TRACKER** (*optional, default: false*): Boolean variable that defines either azk should track deploy anonymous data or not;
- **ENV_FILE** (*optional, default: `.env`*): The `.env file` path that will be copied to remote server;
- **SSH_KEY_NAME** (*optional, default: form public key*): The key name used for DigitalOcean to identify a key. By default, it's extracted from the SSH public key.

#### Usage

Consider you want to deploy your app into DigitalOcean and your local .ssh keys are placed at `LOCAL_DOT_SSH_PATH` (usually this path is `$HOME`/.ssh).

#### Usage with `azk`

Example of using this image with [azk](http://azk.io):

- Add the `deploy` system to your Azkfile.js:

```js
/**
 * Documentation: http://docs.azk.io/Azkfile.js
 */

// Adds the systems that shape your system
systems({
  // ...

  deploy: {
    image: {"docker": "azukiapp/deploy-digitalocean"},
    mounts: {
      "/azk/deploy/src":     path("."),
      "/azk/deploy/.ssh":    path("#{env.HOME}/.ssh"),
      "/azk/deploy/.config": persistent("deploy-config"),
    },
    scalable: {"default": 0, "limit": 0},
  },
});
```

- Add the `HOST_DOMAIN` (if any) and `HOST_IP` var to your main system http domains (so you can access it by http://`SERVER_PUBLIC_IP` or http://`YOUR_CUSTOM_DOMAIN`). Please note the order matter.

```js
/**
 * Documentation: http://docs.azk.io/Azkfile.js
 */

// Adds the systems that shape your system
systems({
  example: {
    // ...
    http: {
      domains: [
        // ...
        "#{env.HOST_DOMAIN}",
        "#{env.HOST_IP}"
      ]
    },
  },

  // ...
});
```

- Add your [DigitalOcean API][do-api-token] token into `.env` file:
```bash
$ echo DEPLOY_API_TOKEN=PUT_YOUR_TOKEN_HERE >> .env
```

- Run:
```bash
$ azk deploy
```

- Customizing `AZK_RESTART_COMMAND` for a specific deploy:
```bash
$ azk deploy -e AZK_RESTART_COMMAND="azk restart -R -vvvv --rebuild"
```

#### Usage with `docker`

To create the image `azukiapp/deploy-digitalocean`, execute the following command on the deploy-digitalocean image folder:

```sh
$ docker build -t azukiapp/deploy-digitalocean latest
```

To run the image:

```sh
$ docker run --rm --name deploy-digitalocean-run \
  -v $(pwd):/azk/deploy/src \
  -v $HOME/.ssh:/azk/deploy/.ssh \
  -e "DEPLOY_API_TOKEN=`DIGITALOCEAN_API_TOKEN`" \
  azukiapp/deploy-digitalocean
```

Before running, replace `DIGITALOCEAN_API_TOKEN` with the actual value.


## License

Azuki Dockerfiles distributed under the [Apache License](https://github.com/azukiapp/docker-deploy-digitalocean/blob/master/LICENSE).

[do-api-token]: https://cloud.digitalocean.com/settings/applications

[azukiapp/deploy-digitalocean](http://images.azk.io/#/deploy-digitalocean)
==================

Base docker image to deploy an app into DigitalOcean using [`azk`](http://azk.io)

Versions (tags)
---

<versions>
- [`latest`](https://github.com/azukiapp/docker-deploy-digitalocean/blob/master/latest/Dockerfile)
</versions>

Image content:
---

- Ubuntu 14.04
- [Ansible](http://www.ansible.com)
- [SSHPass](http://sourceforge.net/projects/sshpass/)
- [python-digitalocean](https://github.com/koalalorenzo/python-digitalocean)

### Configuration
The following environment variables are available for configuring the deployment using this image:

- **API_TOKEN**: User's API token in DigitalOcean;
- **LOCAL_PROJECT_PATH**: (*optional, default: /azk/deploy/src*) Project source code path;
- **LOCAL_DOT_SSH_PATH** (*optional, default: /azk/deploy/.ssh*): Path containing SSH keys. If no path is given, a new SSH public/private key pair will be generated;
- **REMOTE_USER** (*optional, default: git*): Username created (or used if it exists) in the remote server to deploy files and run the app;
- **AZK_DOMAIN** (*optional, default: azk.dev.io*): azk domain in the current namespace;
- **REMOTE_PROJECT_PATH_ID** (*optional*): By default, the project will be placed at */home/`REMOTE_USER`/`REMOTE_PROJECT_PATH_ID`* (i.e., `REMOTE_PROJECT_PATH`) in the remote server. If no value is given, a random id will be generated;
- **REMOTE_PROJECT_PATH** (*optional*): The path where the project will be stored in the remote server. If no value is given, it will be */home/`REMOTE_USER`/`REMOTE_PROJECT_PATH_ID`*;
- **RUN_SETUP** (*optional, default: true*): Boolean variable that defines if the remote server setup step should be run;
- **RUN_DEPLOY** (*optional, default: true*): Boolean variable that defines if the deploy step should be run;

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
      "/azk/deploy/src":  path("."),
      "/azk/deploy/.ssh": path("`LOCAL_DOT_SSH_PATH`")
    },
    scalable: {"default": 0, "limit": 0},
    envs: {
      API_TOKEN: "`DO_API_TOKEN`",
    },
  },
});
```

- Run:
```bash
$ azk shell deploy
```

#### Usage with `docker`

To create the image `azukiapp/deploy-digitalocean`, execute the following command on the deploy-digitalocean image folder:

```sh
$ docker build -t azukiapp/deploy-digitalocean .
```

To run the image:

```sh
$ docker run --rm --name deploy-digitalocean-run \
  -v `LOCAL_PROJECT_PATH`:/azk/deploy/src \
  -v `LOCAL_DOT_SSH_PATH`:/azk/deploy/.ssh \
  -e "API_TOKEN=`DO_API_TOKEN`" \
  azukiapp/deploy-digitalocean
```

## License

Azuki Dockerfiles distributed under the [Apache License](https://github.com/azukiapp/docker-deploy-digitalocean/blob/master/LICENSE).

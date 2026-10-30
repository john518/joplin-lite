# Joplin Server Setup

The Joplin Lite application connects to Joplin through the same backend as the Joplin Desktop and Terminal applications. It is called the Joplin Data/API server. So to use Joplin Lite, you must install Joplin.

- You do NOT need to install the full Joplin Desktop application, which is built on the Electron platform and has a heavy memory and storage footprint.
- You can instead install the much-smaller terminal application

The steps for installing via the terminal application are as follows.

## 1. Install the Joplin Terminal Application

The instructions for installing the terminal application are shown near the top of [https://joplinapp.org/help/apps/terminal/](https://joplinapp.org/help/apps/terminal/).

Note that if you are installing Joplin for personal use, you can skip the step to create a system link at `usr/local/bin`, and instead create a symbolic link in your directory at `$HOME/.local/bin/joplin`.

## 2. Run the server to create a joplin-lite profile

To avoid conflicts with other Joplin applications, create a "joplin-lite" profile by starting the server. From your $HOME directory:

```bash
mkdir -p ~/.config/joplin-lite
joplin --profile ~/.config/joplin-lite server start

```

## 3. Stop the server so that we can edit the settings.json

You can Control-C to stop the server, or you can open a second terminal and issue this command:

```bash
joplin --profile ~/.config/joplin-lite server stop

```

## 4. Edit the profile settings file to change the port number

To avoid conflict with the terminal app, add a new field to the settings file at `$HOME/.config/joplin-lite/settings.json` to change the port number from the default (41184) to 41183. Add this element to the file, just before the "api.token" field:

```json
"api.port": 41183,

```

Note: we originally used 44185, however, we want a port number **outside** the range used by other Joplin apps (41184 to 41185).

## 5. Check that the server is running

Restart the server using the same command as in step 2:

```bash
joplin --profile ~/.config/joplin-lite server start

```

To double check we are configured OK, open a second terminal and, from your $HOME directory, run:

```bash
joplin --profile ~/.config/joplin-lite server status

```

The command should return the message `Server is running on port 41183`

## 6. [Optional] Configure synchronization with remote store

If you are already use a remote store for existing Joplin notes, use the `joplin config` commands to set up synchronization with your remote store. To start, use the command `joplin --profile ~/.config/joplin-lite config sync.target` to get the list of sync targets and their corresponding id number. In my case, I have installed the Joplin Cloud server on my local network. The "Joplin Server" target number is 9, so my commands look like this:

```bash
joplin --profile ~/.config/joplin-lite config sync.target 9
joplin --profile ~/.config/joplin-lite config sync.9.path http://<ip-of-remote-server>:22300
joplin --profile ~/.config/joplin-lite config sync.9.username "me@example.com"
joplin --profile ~/.config/joplin-lite config sync.9.password "my-password"

```

# 7. Restart the server to sync with the remote

- From a second terminal, stop the server with the same command as before: `joplin --profile ~/.config/joplin-lite server stop`.
- From the first terminal, restart the server with the same command as before: `joplin --profile ~/.config/joplin-lite start`
- From the second terminal, give the command to sync: `joplin --profile ~/.config/joplin-lite sync`

The system should begin downloading data from the remote and populating the profile `database.sqlite` file.

## 8. OPTIONAL/TBD: Configure the system to start the server on login

I am not sure this is worth the effort, but you can configure the system to start the joplin server when you login.

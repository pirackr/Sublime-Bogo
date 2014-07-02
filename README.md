Sublime-BoGo
============

Vietnamese input method for Sublime Text 2 and 3 using the
[BoGo engine](https://github.com/BoGoEngine/bogo-python).

Installation
============

The preferred way to install this plugin is through Package Control. 
[Install it][1] and [search for **BoGo**][2]. Package Control will 
handle automatic update so you don't have to.

Of course, if you want, manually installation is possible as well:

```bash
$ cd ~/.config/sublime-text-3/Packages/
$ git clone https://github.com/pirackr/Sublime-Bogo.git
```

Every once in a while, you can update it with the following commands:

```bash
$ cd ~/.config/sublime-text-3/Packages/Sublime-Bogo
$ git reset --hard
$ git pull origin master
```

[1]: https://sublime.wbond.net/installation
[2]: https://sublime.wbond.net/docs/usage

Configuration
=============

After installing, your status line will update to say **BoGo: ON** or **BoGo:
OFF**. The default hotkey to turn it on/off is `Alt + Z`. You can change it
through the `Default.sublime-keymap` file:

```json
[
	{ "keys": ["alt+z"], "command": "bogo_enable_toggle" }
]
```

BoGo supports the Telex and Vni typing styles, with Telex being the default.
If you want to change it, edit `Bogo.sublime-settings`:

```json
{
    "bogo-rule" : "Telex"
}
```

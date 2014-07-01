Sublime-Bogo
============

Vietnamese input method for Sublime Text 2 and 3 using the
[BoGo engine](https://github.com/BoGoEngine/bogo-python).

Installing
==========

We now support installation through Package Control, which can be found at this site: http://wbond.net/sublime_packages/package_control

Once you install Package Control, restart Sublime Text and bring up the Command Palette (Command+Shift+P on OS X, Control+Shift+P on Linux/Windows). Select "Package Control: Install Package", wait while Package Control fetches the latest package list, then select Bogo when the list appears. The advantage of using this method is that Package Control will automatically keep Bogo up to date with the latest version.

If you don't want to install Package Control plugin, you are still be able to use Bogo by manuall installation:

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
Configuring
===========

Default hotkey to turn on/off Bogo is ``Alt + Z``. You can change it through sublime-keymap file:

```
[
	{ "keys": ["alt+z"], "command": "bogo_enable_toggle" }
]
```

Bogo support Telex and Vni typing style, default one is Telex, so if you want to change it, edit the Bogo settings file (Bogo.sublime-settings):
```
{
    "bogo-rule" : "Telex"
}
```

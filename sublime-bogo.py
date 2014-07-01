import sys
import sublime
import sublime_plugin
import os
from itertools import takewhile
import string

sys.path.append(os.path.join(os.path.dirname(__file__), 'bogo/'))
from bogo import core


ENABLED = True
LISTENER = None


def only_if_enabled(function):
    def inner(*args, **kwargs):
        if ENABLED:
            return function(*args, **kwargs)

    return inner


class BogoListener(sublime_plugin.EventListener):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        global LISTENER
        self.other_command = False
        self.editing_lock = False
        LISTENER = self

    # This gets called every time the cursor is moved and is where we detect
    # user's key presses.
    @only_if_enabled
    def on_selection_modified(self, view):

        if self.editing_lock:
            return

        # If a special command happens (left_delete, move,...),
        # on_window_command and on_text_command is always called first.
        # We don't care about special commands, just regular key presses.
        if self.other_command:
            self.other_command = False
            return

        view = sublime.active_window().active_view()

        # FIXME: Abstract this into a context manager?
        self.editing_lock = True

        # Find the char that has just been typed in
        cursor = view.sel()[0]
        if cursor.begin() == cursor.end():
            cursor = sublime.Region(cursor.begin() - 1, cursor.end())
            new_char = view.substr(cursor)

            # Delete that new char
            view.run_command('left_delete')

            bogo_args = {
                "command": "new_char",
                "args": {
                    "char": new_char
                }
            }
            view.run_command('bogo', bogo_args)

        self.editing_lock = False

    @only_if_enabled
    def on_window_command(self, window, command_name, args):
        self.other_command = True

    @only_if_enabled
    def on_text_command(self, view, command_name, args):
        """
        Intercepts text commands before they actually run.

        Return
            None if we want to let the command run or a tuple of the form
            ('command_name', {'args':'value'}) to specify a different command
            to run instead of it.
        """
        self.other_command = True
        self.new_text_command = None

        self.editing_lock = True

        if command_name == "left_delete":
            view.run_command('bogo', {"command": command_name})
        else:
            view.run_command('bogo', {'command': 'reset'})

        self.editing_lock = False
        return self.new_text_command

    # This will be called by the BogoCommand to determine whether we
    # should swallow this text_command.
    def on_text_command_callback(self, new_command):
        self.new_text_command = new_command


class BogoEnableToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global ENABLED
        if ENABLED:
            ENABLED = False
        else:
            ENABLED = True
        self.view.set_status('BogoEnabled', str(ENABLED))


class BogoCommand(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset()

    def reset(self):
        self.sequence = ""
        self.previously_committed_string = ""

    def accepted_chars(self):
        if sys.version_info[0] > 2:
            accepted_chars = \
                string.ascii_letters + \
                ''.join(self.getRule().keys())
        else:
            accepted_chars = \
                string.lowercase + \
                string.uppercase + \
                ''.join(self.getRule().keys())

        return accepted_chars

    # Command dispatcher
    def run(self, edit, command, args={}):
        self.edit = edit

        if command == "new_char":
            self.on_new_char(args["char"])
        elif command == "reset":
            self.reset()
        elif command == "left_delete":
            self.on_left_delete()

    def on_new_char(self, char):
        if not char in self.accepted_chars():
            self.reset()
            self.commit(char)
            self.reset()
        else:
            if self.sequence == "" and len(self.view.sel()) == 1:
                # Try to continue from the existing string at the cursor
                # position only if there is only one cursor.
                # Things would get weird if there are several cursors
                # with different words under each.
                word_under_cursor = self.view.substr(
                    self.view.word(self.view.sel()[0]))

                if word_under_cursor.isalpha():
                    self.sequence = word_under_cursor

                self.previously_committed_string = self.sequence

            self.sequence += char
            result = core.process_sequence(self.sequence)
            self.commit(result)

    def on_left_delete(self):
        self.sequence = self.sequence[:-1]
        if self.sequence == "":
            self.reset()
        else:
            result = core.process_sequence(self.sequence)
            self.commit(result)

            # NOTE blank_command is just a made up command. It doesn't exist
            # (at least I think it doesn't) so ST will do nothing.
            LISTENER.on_text_command_callback(("blank_command", {}))

    def commit(self, string):
        same_initial_chars = list(
            takewhile(lambda tupl: tupl[0] == tupl[1],
                      zip(self.previously_committed_string,
                          string)))

        chars_to_delete = len(
            self.previously_committed_string) - len(same_initial_chars)

        # We have multiple cursors.
        for cursor in self.view.sel():
            replace_region = sublime.Region(
                cursor.begin() - chars_to_delete, cursor.end())
            replace_with = string[len(same_initial_chars):]

            self.view.erase(self.edit, replace_region)
            self.view.insert(self.edit, replace_region.begin(), replace_with)

        self.previously_committed_string = string

    def getRule(self):
        """
        Get bogo rule definition from setting

        Parameters
        ----------

        Return
        ------
        definition : dict
            A dictionary of bogo rule definition, be used as parameter of
            process_key() method.
        """
        # cast setting to str, then in case users give a wrong input, it should
        # fallback to Telex rule
        bogoRule = \
            str(sublime.load_settings('Bogo.sublime-settings')
                .get('bogo-rule')).upper()

        if bogoRule == 'VNI':
            return core.get_vni_definition()
        else:
            return core.get_telex_definition()

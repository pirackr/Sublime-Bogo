import sys
import sublime
import sublime_plugin
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'bogo/'))
from bogo import core


STATUS = True
MODIFIED = False


class BogoListener(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        global STATUS, MODIFIED

        if not STATUS:
            return

        if not MODIFIED:
            view.run_command('bogo')

        MODIFIED = False


class BogoEnableToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global STATUS
        if STATUS:
            STATUS = False
        else:
            STATUS = True
        self.view.set_status('BogoEnabled', str(STATUS))


class BogoCommand(sublime_plugin.TextCommand):
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
        bogoRule =\
            str(sublime.load_settings('Bogo.sublime-settings')
                .get('bogo-rule')).upper()

        if bogoRule == 'VNI':
            return core.get_vni_definition()
        else:
            return core.get_telex_definition()

    # Text command which replace Vietnamese
    def run(self, edit):
        global MODIFIED
        selections = self.view.sel()

        if not selections:
            return

        # Get current word
        for selection in selections:
            region = self.view.word(selection)
            st = self.view.substr(region)

            if len(st) > 0:
                replace = core.process_sequence(st, self.getRule())
                # Ok, it's a Vietnamese input
                if replace != st:
                    self.view.replace(edit, region, replace)
                    MODIFIED = True

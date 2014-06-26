import sys
import sublime, sublime_plugin
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'bogo/'))
from bogo import core


STATUS = True 
MODIFIED = False
RULE = 'Telex'


class BogoListener(sublime_plugin.EventListener):
    def on_modified(self, view):
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


class BogoChangeRuleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global RULE
        if RULE == 'Telex':
            RULE = 'VNI'
        else:
            RULE = 'Telex'
        self.view.set_status('BogoRule', RULE)


class BogoCommand(sublime_plugin.TextCommand):
    # Text command which replace Vietnamese
    def run(self, edit):
        global MODIFIED, RULE
        selections = self.view.sel()

        if not selections:
            return

        # Get current word
        selection = selections[0]
        region = self.view.word(selection)
        st = self.view.substr(region)

        if RULE == 'Telex':
            rule = core.get_telex_definition()
        else:
            rule = core.get_vni_definition()

        if len(st) > 0:
            replace = core.process_sequence(st, rule)
            # Ok, it's a Vietnamese input
            if replace != st:
                self.view.replace(edit, region, replace)
                MODIFIED = True

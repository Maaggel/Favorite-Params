# Author-Mikkel Bjørnmose Bundgaard
# Description-Makes it easy to manage all favorite User Parameters, grouped and sorted alphabetically

# Import commands - you can add more than one
from .FavoriteParamsCommand import FavoriteParamsCommand

# Preset
commands = []
command_definitions = []

# Define parameters for the commands
cmd = {
    'cmd_name': 'Favorite Params',
    'cmd_description': 'Enables you to edit all favorite User Parameters, grouped and sorted alphabetically',
    'cmd_resources': './resources',
    'cmd_id': 'cmdID_FavoriteParams',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'SolidModifyPanel',
    'class': FavoriteParamsCommand
}
command_definitions.append(cmd)

# Main content - don't change this
for cmd_def in command_definitions:
    command = cmd_def['class'](cmd_def, False) #Change to True to debug the code
    commands.append(command)

# On run
def run(context):
    for run_command in commands:
        run_command.on_run()

# On stop
def stop(context):
    for stop_command in commands:
        stop_command.on_stop()

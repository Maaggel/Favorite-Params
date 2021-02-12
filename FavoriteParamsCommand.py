__author__ = 'maaggel'

# Import modules
import adsk.core
import adsk.fusion
import traceback
from .Fusion360Utilities.Fusion360Utilities import get_app_objects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase

# Main command class
class FavoriteParamsCommand(Fusion360CommandBase):
    #Trigger on preview
    def on_preview(self, command, inputs, args, input_values):
        update_favorite_params(inputs)

    # Trigger on execute
    def on_execute(self, command, inputs, args, input_values):
        update_favorite_params(inputs)

    # Trigger on create
    def on_create(self, command, inputs):
        # Gets necessary application objects from utility function
        app_objects = get_app_objects()
        design = app_objects['design']

        # Get and sort the params
        userParams = sorted(design.userParameters, key=lambda x: x.name)

        # Preset
        lastGroupName = ""
        currentGroup = False
        hasGroups = False
        undefinedGroup = False

        # Do we have any groups?
        for param in userParams:
            # Favorite?
            if(param.isFavorite):
                # Is this a group?
                if(param.name.find("__") != -1):
                    hasGroups = True

        # Loop through the params, and add them if they are favorites
        # - Grouped only
        for param in userParams:
            # Favorite?
            if(param.isFavorite):
                # Is this a group?
                if(param.name.find("__") != -1):
                    # Get the params
                    splitName = param.name.split("__")
                    groupName = splitName[0]

                    # Get pretty name - Camel case
                    prettyGroupName = ' '.join(split_on_uppercase(splitName[0], True))
                    prettyName = ' '.join(split_on_uppercase(splitName[1], True))

                    # Get pretty name - Snake case
                    prettyGroupName = ' '.join(prettyGroupName.split('_'))
                    prettyName = ' '.join(prettyName.split('_'))

                    # Add the group if not there
                    if(lastGroupName != groupName):
                        lastGroupName = groupName
                        currentGroup = inputs.addGroupCommandInput('group_label_'+groupName, prettyGroupName)
                        currentGroup.isExpanded = True
                    
                    # Add this to the group
                    currentGroup.children.addStringValueInput(param.name,
                                            prettyName,
                                            param.expression)

        # Loop through the params, and add them if they are favorites
        # - Not Grouped only
        for param in userParams:
            # Favorite?
            if(param.isFavorite):
                # Is this a group?
                if(param.name.find("__") == -1):
                    # Get pretty name - Camel case
                    prettyName = ' '.join(split_on_uppercase(param.name, True))

                    # Get pretty name - Snake case
                    prettyName = ' '.join(prettyName.split('_'))

                    # Do we have any groups?
                    if(hasGroups):
                        # Create "Ungrouped" group?
                        if(undefinedGroup == False):
                            undefinedGroup = inputs.addGroupCommandInput('group_label_undefined', "Not Grouped")
                            undefinedGroup.isExpanded = True

                        # Add this
                        undefinedGroup.children.addStringValueInput(param.name,
                                                prettyName,
                                                param.expression)
                    else:
                        # Add this
                        inputs.addStringValueInput(param.name,
                                                prettyName,
                                                param.expression)

# Update params
def update_favorite_params(inputs):
    # Gets application objects
    app_objects = get_app_objects()
    design = app_objects['design']
    units_manager = app_objects['units_manager']

    # No favorite params?
    if(inputs.count == 0):
        app_objects['ui'].messageBox('The model doesn\'t have any favorited user parameters')
        return

    # Set all parameter values based on the input form
    for param in design.userParameters:
        if(param.isFavorite):
            # Get the expression
            input_expression = inputs.itemById(param.name).value

            # Use Fusion Units Manager to validate user expression
            if(units_manager.isValidExpression(input_expression, units_manager.defaultLengthUnits)):
                param.expression = input_expression
            else:
                app_objects['ui'].messageBox('The following expression is invalid: \n' +
                                            param.name + '\n' +
                                            input_expression)

# Split on uppercase
def split_on_uppercase(s, keep_contiguous=False):
    string_length = len(s)
    is_lower_around = (lambda: s[i-1].islower() or 
                       string_length > (i + 1) and s[i + 1].islower())

    start = 0
    parts = []
    for i in range(1, string_length):
        if s[i].isupper() and (not keep_contiguous or is_lower_around()):
            parts.append(s[start: i])
            start = i
    parts.append(s[start:])

    return parts
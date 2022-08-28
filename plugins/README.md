# Plugins

## Overview

Plugins are derived from the plugins._dreamplugin.DreamPlugin abstract base class.  They
implement three interface methods: `__init__`, `get_dream_prompt`, and `process_dream_output`.  Instances of
these classes are created dynamically and their methods are executed
iteratively, based on the state of the "dream>" parser (either requesting
"dream>" console input or processing output results.)

The `__init__` method accepts a Python list of the initial switches.  These
are the switches that the user enters at the "dream>" and can contain a
mix of plug-in specific switches along with the standard "dream>"-style
switches for control.  These switches are processed via two
separate parsers using the `parse_known_args` method to drop any
unrecognized inputs.

The `get_dream_prompt` method is called by the "dream>" console when it wishes
to consume input from the plugin.  This is a normalized output string that
mimics something a user can enter via keyboard.  The plugin should pass
"--terminate-plug" to end operation.

The `process_dream_output` method is invoked by "dream>" to pass run
results for an iteration.  These results are in the form of a
Python list.  This method may be called once or multiple times depending
on the switches passed to plugin.

Note: previous

## Invocation

From the 'dream>' console, call the plugin using the `--plugin` option
and include any config and image parameters as desired.  Example:

	dream> black dragon flying, color illustration -W768 -H512 --plugin plugins.iteratecfgscale --cs_start 8.0 --cs_stop 10.0 --cs_step 0.5

For this plugin example, the standard parameters `-W` and `-H` will be passed by the plugin
to the "dream>" prompt, and the plugin will use the `cs_*` switches to sweep the
cfg_scale from 8.0 -> 10.0 in 0.5 increments.

## Creating new plugins

- Copy the `plugins._template.py` to `plugins/` with the plugin name.
- Update the `plugin_class_name` line and name of the class
- Update the `__init__`, `get_dream_prompt`, and `process_dream_output` methods
- Define a custom `plugin_parser` method for any unique options the plugin requires
- Execute new plugin via the "dream>" console. Example: `dream> black dragon, flying -S 123456 --plugin plugins.my_shiny_new_plugin`

Since plugins are loaded dynamically at run-time, they can be updated without have to restart `dream.py`.


# Easy_Command_Runner
A small deep learning tool with GUI for generating commands (e.g. hyper-parameter setting for deeplearning) and adaptively running commands with GPU whenever the GPU memory is free enough.

# Usage
There are mainly two parts of this tool: 1) Command Generator, 2) GPUScheduler. The first one is for generating all the wanted combinations of parameters. The second one is for running commands automatically whenever GPU device is available.

## Generator
### ECG with GUI
Run `ECG_GUI.py` or click the 'main.exe' and the tool will be like this
<p>
  <img src="https://github.com/WwZzz/myfigs/blob/master/ECG_1.png" width="500" />
</p>

There are three buttons on the screen, whose function are as below:
  * `AddLine`: adds the new parameter for the commands to be generated as a new line
  * `Generate`: generate the commands according to the current input
  * `Clear`: clear out all the added lines and the generated text of commands on the screen

The content of the entries `Command Head` and `Command End` will appear at the head or the tail of all the generated commands. For example, if `Command Head`=`python`, then every command will start with 'python'. The usage of `Command End` is the same.

After pressing the button `AddLine`, there will be a few components well organized within a row below the buttons like this:
<p>
  <img src="https://github.com/WwZzz/myfigs/blob/master/ECG_3.png" width="500" /> 
</p>

* `Parameter`: the name of the parameter
* `Value`: the data type (e.g. int, flt, str) and the value (list, range, or single value)
* `Del`: delete the current row
* `Used Iteratively`: if this term is selected, the current parameter will be inserted into all the generated commands with only a value in a iterative manner. For example, if the parameter is `--gpu` and the value is '0,1,2', then each command will contains `--gpu {}` where {} is one of {0,1,2}.

Now, we show the full function by the example below
<p>
  <img src="https://github.com/WwZzz/myfigs/blob/master/ECG_2.png" width="500" /> 
</p>
<p>
We only implement very basic functions by strings analysis, which supports to specify the value of the parameters as:
</p>

* if the value starts with '\[' or '{', it's considered as a list of values which is spilted by ',' . (e.g. \[1,2,3], {SGD, ADAM})
* if the value starts with '(', it's considered as a tuple `(left, right, interval)` like the `range(...)` in python. (e.g. (1,5,1) = {1,2,3,4,5})
* if the value starts with digits or '-', it can be a single digit value or a list of values spilted by ',' (e.g. 1,2,3 = \[1,2,3])
* the value is considered as single value for the rest cases. (e.g. mnist)

<p>
Finally, we also allow the tool to save current settings as `config.json`, and the saved configuration can be used again for the next time.
</p>

* `file>save`: save the current config into a file
* `file>load`: load the config from file

The architecture of the saved configuration is
```python
"""
{
    '__command_head': ''
    '__command_end': ''
    'parameter_name': [type:str, value: str, used_iteratively: int]
    ...
}
"""
```

### ECG without GUI
ECG without GUI can read `config.json` and convert it into the text of commands. The usage of this program is
```sh
python ECG.py config_file command_text_file
```
The architecture of the config file is the same as the saving manner of ECG_GUI.

## GPUScheduler

GPUScheduler is for automatically running commands whenever GPU is free enough. Before using this tool, everyone should confirm the correctness of the command for which can be carried out succefully without this tool, including correctly exit with code 0. There are six parameters to be specified (one required and five optional):
* `cmd_file`: the name of the text file which contains all the commands to be carried and is required
* `m`: the least memory needed for each command (MB)
* `p`: the period of confirming the GPU is being adequately free (seconds)
* `i`: the interval between every two checking frames and should be smaller that `p` (seconds)
* `d`: the working dictionary of the commands
* `b`: the bin path of the commands, which is useful when the python interpreter is created by anaconda. 

The usage of this file is
```sh
python GPUScheduler.py command_file --m 1000 --p 30 --i 10 --d project_path --b anaconda_interpreter_path 
```
And a table like this will appear on the screen before all the commands are finished:
<p>
  <img src="https://github.com/WwZzz/myfigs/blob/master/ECG_4.png" width="500" /> 
</p>


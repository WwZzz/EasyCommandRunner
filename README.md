# Easy_Command_Runner
A small tool with GUI for generating commands (e.g. hyper-parameter setting for deeplearning) and adaptively running commands with GPU when the GPU memory is free enough.

# Usage
There are mainly two parts of this tool: 1) Command Generator, 2) GPUScheduler.

## Generator
### ECG with GUI
Run `ECG_GUI.py` or click the 'main.exe' and the tool will be like this
<p>
  <img src="https://github.com/WwZzz/myfigs/blob/master/ECG_1.png" width="500" />
</p>

There are three buttons on the screen, whose function are as below:

* AddLine: adds the new parameter for the commands to be generated as a new line
* Generate: generate the commands according to the current input
* Clear: clear out all the added lines and the generated text of commands on the screen

The content of the entries `Command Head` and `Command End` will appear at the head or the tail of all the generated commands. For example, if `Command Head`=`python`, then every command will start with 'python'. The usage of `Command End` is the same.

After pressing the button `AddLine`, there will be a few components well organized within a row below the buttons like this:


For valu with a row es in 'Value', the tool combinates the lists of different parameters into a grid of parameters. The result is as below.
<p>
  <img src="https://github.com/WwZzz/myfigs/blob/master/ECG_2.png" width="500" /> 
</p>
<p>
There are three types of value: int, str, flt. And the rules of the input is simply designed by the starting char:
  
  '(': (left_flag, right_flag, interval)
  
  '[': list
  
  '{': The same as '['
  
  digits or '-': single value or lists of values
  
  letters: the type must be string
  
</p>

button clear: clear all the settings

button addline: add another parameter below

generate: output the commands on the screen

file>save: save the current config into a file

file>load: load the config from file

The option 'UsedIteratively' ensures the variable not to generate as the grid but an iteratively used one across the commands.

# Easy_Command_Generator
A small tool with GUI for generating commands (e.g. hyper-parameter setting for deeplearning).

# Usage
The initial state of the tool.
<p>
  <img src="https://github.com/WwZzz/myfigs/blob/master/ECG_1.png" width="500" />
</p>

For values in 'Value', the tool combinates the lists of different parameters into a grid of parameters. The result is as below.
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

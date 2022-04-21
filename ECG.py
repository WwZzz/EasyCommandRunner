import json
import copy
import sys

def load_config(path = 'config.json'):
    with open(path, 'r') as inf:
        config = json.load(inf)
    return config

def analyze_value(pval, type='flt'):
    pval = pval.strip().replace(" ", "")
    if type == 'flt':
        if pval.startswith("(") and pval.endswith(")"):
            pval = pval[1:-1]
            pval = pval.split(',')
            pval = [float(v) for v in pval]
            l, r, interval = pval[0], pval[1], pval[2]
            pval = []
            while l<=r:
                pval.append(l)
                l+=interval
        elif pval.startswith("[") and pval.endswith("]"):
            pval = pval[1:-1]
            pval = pval.split(',')
            pval = [float(v) for v in pval]
        elif pval.startswith("{") and pval.endswith("}"):
            pval = pval[1:-1]
            pval = pval.split(',')
            pval = [float(v) for v in pval]
        elif ord('0')<=ord(pval[0])<=ord('9') or pval[0]=='-':
            if pval.find(',')>-1:
                pval = pval.split(',')
                pval = [float(v) for v in pval]
            else:
                pval = [float(pval)]
        else:
            pval = [pval]
    elif type=='str':
        if pval.startswith("[") and pval.endswith("]"):
            pval = pval[1:-1]
            pval = pval.split(',')
        elif pval.startswith("{") and pval.endswith("}"):
            pval = pval[1:-1]
            pval = pval.split(',')
        else:
            pval = [pval]
    elif type=='int':
        if pval.startswith("(") and pval.endswith(")"):
            pval = pval[1:-1]
            pval = pval.split(',')
            pval = [int(v) for v in pval]
            l, r, interval = pval[0], pval[1], pval[2]
            pval = []
            while l<=r:
                pval.append(l)
                l+=interval
        elif pval.startswith("[") and pval.endswith("]"):
            pval = pval[1:-1]
            pval = pval.split(',')
            pval = [int(v) for v in pval]
        elif pval.startswith("{") and pval.endswith("}"):
            pval = pval[1:-1]
            pval = pval.split(',')
            pval = [int(v) for v in pval]
        elif ord('0')<=ord(pval[0])<=ord('9') or pval[0]=='-':
            if pval.find(',')>-1:
                pval = pval.split(',')
                pval = [int(v) for v in pval]
            else:
                pval = [int(pval)]
        else:
            pval = [int(pval)]
    return pval

filepath = 'config.json'
outputfile = 'cmds'
if len(sys.argv)==2:
    filepath = sys.argv[1]
if len(sys.argv)==3:
    outputfile = sys.argv[2]

con = load_config()
cmds = [[con['__command_head']]]
for paraname, v in con.items():
    if paraname=='__command_head' or paraname=='__command_end':
        continue
    vtype, vals, UsedIteratively = v[0], v[1], v[2]
    vals = analyze_value(vals, vtype)
    if UsedIteratively == 1:
        k = 0
        for cmd in cmds:
            cmd.append(paraname + " " + str(vals[k]))
            k = (k + 1) % len(vals)
    else:
        num_cmd_per_val = len(cmds)
        l = [copy.deepcopy(cmds) for _ in range(len(vals))]
        cmds = []
        for li in l:
            cmds = cmds + li
        start_cmd = 0
        for val in vals:
            for k in range(num_cmd_per_val):
                cmds[start_cmd + k].append(paraname + " " + str(val))
            start_cmd += num_cmd_per_val
end_string = con['__command_end']
cmds = [" ".join(cmd) + " " + end_string+ '\n' for cmd in cmds]

with open(outputfile, 'w') as outf:
    outf.writelines(cmds)


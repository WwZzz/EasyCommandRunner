import json
import tkinter.filedialog
from tkinter import *
from tkinter import messagebox
import copy
from tkinter import ttk

class Line:
    def __init__(self, root):
        self.frame = Frame(root)
        self.visible = False
        self.UsedIteratively = IntVar()
        self.type = StringVar()
        self.dict = {
            "lb_para": Label(self.frame, text = 'Parameter: '),
            "en_para": Entry(self.frame),
            "lb_val":Label(self.frame, text='Value: '),
            "combo": ttk.Combobox(self.frame, width=3, textvariable=self.type),
            "en_val": Entry(self.frame),
            "btn_del": Button(self.frame, text="Del", command=self.unpack),
            "chk_iterate": Checkbutton(self.frame, text="Used Iteratively", variable=self.UsedIteratively)
        }
        self.dict['combo']['value']=['str', 'flt', 'int']
        self.dict['combo'].current(1)
        for k in self.dict.keys():
            self.dict[k].pack(side="left")

    def pack(self):
        self.visible = True
        self.frame.pack(side="top")

    def unpack(self):
        self.visible = False
        self.frame.pack_forget()

class App:
    def __init__(self, root):
        self.root = root
        # menu
        self.menubar = Menu(self.root)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label="Load", command=self.load_config)
        self.file_menu.add_command(label='Save', command=self.save_config)
        self.root['menu']=self.menubar

        # btn_frame for the first line
        self.btn_frame = Frame(self.root)
        self.btn_AddLine = Button(self.btn_frame, text="AddLine", command=self.add_line)
        self.btn_Gen = Button(self.btn_frame, text="Generate", command=self.generate)
        self.btn_Clear = Button(self.btn_frame, text='Clear', command=self.clear)
        self.NUM_LINES = 100
        self.lines = [Line(self.root) for _ in range(self.NUM_LINES)]
        self.btn_AddLine.pack(side="left")
        self.btn_Gen.pack(side="left")
        self.btn_Clear.pack(side='right')
        self.btn_frame.pack(side="top")

        # side frame for the second line
        self.side_frame = Frame(self.root)
        self.lb_head = Label(self.side_frame, text="Command Head: ")
        self.entry_head = Entry(self.side_frame)
        self.lb_end = Label(self.side_frame, text="Command End: ")
        self.entry_end = Entry(self.side_frame)
        self.lb_head.pack(side='left')
        self.entry_head.pack(side='left')
        self.lb_end.pack(side='left')
        self.entry_end.pack(side='left')
        self.side_frame.pack(side='top')

        # text_frame for the last second line
        self.output_frame = Frame(self.root)
        self.sv = Scrollbar(self.output_frame)
        self.sh = Scrollbar(self.output_frame, orient=HORIZONTAL)
        self.sv.pack(side=RIGHT, fill=Y)
        self.sh.pack(side=BOTTOM, fill=X)
        self.output_text = Text(self.output_frame, yscrollcommand=self.sv, xscrollcommand=self.sh, wrap=NONE)
        self.output_text.pack(expand=YES, fill=BOTH)

        # input frame for the last line
        self.input_frame = Frame(self.root)
        self.input_frame.pack(side='top')

    def clear(self):
        self.entry_head.delete(0,END)
        self.entry_end.delete(0,END)
        for line in self.lines:
            if line.visible==True:
                line.unpack()
        self.lines=[]
        self.output_text.delete(1.0,END)
        self.output_frame.pack_forget()

    def add_line(self):
        self.lines.append(Line(self.input_frame))
        self.lines[-1].pack()
        return

    def load_config(self):
        path = tkinter.filedialog.askopenfilename()
        with open(path, 'r') as inf:
            config = json.load(inf)
        self.clear()
        self.entry_head.insert(0, config['__command_head'])
        self.entry_end.insert(0, config['__command_end'])
        for para, items in config.items():
            if para=='__command_head' or para=='__command_end':
                continue
            self.add_line()
            l = self.lines[-1]
            vtype, val, UsedIteratively = items[0], items[1], items[2]
            l.dict['en_para'].insert(0, para)
            l.type.set(vtype)
            l.dict['en_val'].insert(0, val)
            l.UsedIteratively.set(UsedIteratively)


    def save_config(self):
        path = tkinter.filedialog.asksaveasfilename()
        config = {
            '__command_head': self.entry_head.get(),
            '__command_end':self.entry_end.get()
        }
        for line in self.lines:
            if line.visible==False:
                continue
            paraname = line.dict['en_para'].get()
            paratype = line.type.get()
            paravalue = line.dict['en_val'].get()
            UsedIteratively = line.UsedIteratively.get()
            config[paraname] = (paratype, paravalue, UsedIteratively)
        with open(path, 'w') as outf:
            json.dump(config, outf)

    def generate(self):
        # read dict
        dict = {}
        for line in self.lines:
            if line.visible==False:
                continue
            paraname = line.dict['en_para'].get()
            paravalue = line.dict['en_val'].get()
            # check if the input is correct
            if paraname=="":
                messagebox.showerror(None, "Empty Parameter")
                return
            if paravalue=="":
                messagebox.showerror(None, "Empty Value")
                return
            listvalue = self.analyze_value(paravalue, type=line.type.get())
            dict[paraname] = (listvalue, line.UsedIteratively.get())
        cmds = [[self.entry_head.get()]]
        for paraname, v in dict.items():
            vals = v[0]
            UsedIteratively = v[1]
            if UsedIteratively==1:
                k = 0
                for cmd in cmds:
                    cmd.append(paraname+" "+str(vals[k]))
                    k=(k+1)%len(vals)
            else:
                num_cmd_per_val = len(cmds)
                l = [copy.deepcopy(cmds) for _ in range(len(vals))]
                cmds = []
                for li in l:
                    cmds = cmds + li
                start_cmd=0
                for val in vals:
                    for k in range(num_cmd_per_val):
                        cmds[start_cmd+k].append(paraname+" "+str(val))
                    start_cmd += num_cmd_per_val
        print(cmds)
        self.output_frame.pack(side=BOTTOM)
        self.output_text.delete(1.0,END)
        end_string = self.entry_end.get()
        for i, cmd in enumerate(cmds):
            self.output_text.insert('{}.0'.format(i+1), " ".join(cmd) + " " + end_string + '\n')

    def analyze_value(self, pval, type='flt'):
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
root = Tk()
root.title("Command Generator")
App(root)
root.mainloop()
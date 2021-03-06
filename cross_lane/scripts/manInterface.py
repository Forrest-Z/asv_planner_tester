#!/usr/bin/env python3

#work in progress

import roslaunch
import numpy as np
import datetime
from tkinter import *
import rospkg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def clear_frame(frame):
    for w in frame.winfo_children():
        w.destroy()

class Scenario(object):

    def __init__(self, serial='000000', opus=0, uuid='0'):
        self.uuid = uuid
        # ASV related attributes
        self.angle = None
        self.u_d = None
        self.lp = None
        # Lane related attributes
        self.rlnOb = None
        self.llnOb = None
        self.rlw = None
        self.llw = None
        self.ld = None
        self.rld = None
        self.lld = None
        self.ll = None
        self.dAsv = None #initial and final distance to lanes
        # Output
        self.rospack = rospkg.RosPack()
        self.input = f"{self.rospack.get_path('cross_lane')}/input/{serial}.txt"
        self.output = f"{self.rospack.get_path('cross_lane')}/output/{serial}.txt"
        self.opus = opus

    def graphic_interface(self):

        fenetre = Tk()
        screen_width = fenetre.winfo_screenwidth()
        screen_height = fenetre.winfo_screenheight()
        screen_width = 1920
        screen_height = 1080
        w_big = int(screen_width*5/8)
        w_small = int(screen_width*3/8)
        h_unit = int(screen_height/3)
        fenetre.geometry(f"{screen_width}x{screen_height}")
        fenetre.title("Bench Test")
        fenetre.iconphoto(False, PhotoImage(file=f"{self.rospack.get_path('asv_common')}/images/icon.png"))
        fenetre.configure(bg='gainsboro')

        ###################

        main_frame = Frame(fenetre, width=w_big, height=screen_height)
        main_frame.pack(side=LEFT)
        first_frame = Frame(main_frame, width=w_big, height=2*h_unit)
        first_frame.pack()

        Label(main_frame, text=f'Output: {self.output}', anchor=W, bg='lightslategrey', fg='white').pack(fill='x')
        second_frame = Frame(main_frame, bg='white', width=w_big, height=h_unit)
        second_frame.pack_propagate(0)
        second_frame.pack(fill="both", expand="yes")

        aux_frame = Frame(fenetre, width=w_small, height=screen_height, bg='gainsboro')
        aux_frame.pack(fill='both')
        Label(aux_frame, text='Plot data', bg='lightslategrey', fg='white', width=100).pack()

        ###################
        ###################
        seagull = PhotoImage(file=f"{self.rospack.get_path('asv_common')}/images/Seagull-USV.png")

        canvas = Canvas(first_frame, width=w_big, height=2*h_unit)
        canvas.create_image(w_big/2, 2*h_unit/3, anchor=CENTER, image=seagull)
        canvas.grid(row=0, column=0, rowspan=3, columnspan=3)

        ###################

        l0 = LabelFrame(first_frame, text="ASV", padx=80, pady=40, bg='white')
        l0.grid(row=0, column=1)
        
        angle = DoubleVar()
        angle.set(90.0)
        Label(l0, text="angle (??): ", bg='white', anchor=E).grid(row=0, column=0, sticky="nsew")
        Entry(l0, textvariable=angle, width=5, bg='whitesmoke').grid(row=0, column=1)

        u_d = DoubleVar()
        u_d.set(15.0)
        Label(l0, text="speed (kn): ", bg='white', anchor=E).grid(row=1, column=0, sticky="nsew")
        Entry(l0, textvariable=u_d, width=5, bg='whitesmoke').grid(row=1, column=1)

        lp = IntVar()
        lp.set(1)
        Label(l0, text="Local Planner : ", bg='white', anchor=E).grid(row=2, column=0, sticky="nsew")
        l00 = Frame(l0, bg='white')
        l00.grid(row=2, column=1)
        Radiobutton(l00, variable=lp, text="None", value=0, bg='white', anchor=W, highlightthickness=0).pack(fill='both')
        Radiobutton(l00, variable=lp, text="Velocity Obstacles", value=1, bg='white', anchor=W, highlightthickness=0).pack(fill='both')

        ########################

        l1 = LabelFrame(first_frame, text='Obstacle ship', padx=80, pady=30, bg='white')
        l1.grid(row=1, column=1)
        
        ld = DoubleVar()
        ld.set(200.)
        Label(l1, text="distance between lane (m): ", bg='white', anchor=E).grid(row=0, column=0, sticky="nsew")
        Entry(l1, textvariable=ld, width=5, bg='whitesmoke').grid(row=0, column=1)
        
        dORn = IntVar()
        dORn.set(1)
        Label(l1, text="density or number: ", bg='white', anchor=E).grid(row=1, column=0, sticky="nsew")
        l11 = Frame(l1, bg='white')
        l11.grid(row=1, column=1)
        Radiobutton(l11, variable=dORn, text="density", value=0, bg='white', anchor=W, highlightthickness=0).pack(fill='both')
        Radiobutton(l11, variable=dORn, text="number", value=1, bg='white', anchor=W, highlightthickness=0).pack(fill='both')

        Label(l1, text="width (m): ", bg='white', anchor=E).grid(row=2, column=0, sticky="nsew")
        l10 = Frame(l1, bg='white')
        l10.grid(row=2, column=1)

        rlw = DoubleVar()
        rlw.set(400.)
        Label(l10, text="right lane: ", bg='white', anchor=E).grid(row=0, column=0, sticky="nsew")
        Entry(l10, textvariable=rlw, width=5, bg='whitesmoke').grid(row=0, column=1)

        llw = DoubleVar()
        llw.set(400.)
        Label(l10, text="left lane: ", bg='white', anchor=E).grid(row=1, column=0, sticky="nsew")
        Entry(l10, textvariable=llw, width=5, bg='whitesmoke').grid(row=1, column=1)
        
        Label(l1, text="density (1/hm??): ", bg='white', anchor=E).grid(row=3, column=0, sticky="nsew")
        l12 = Frame(l1, bg='white')
        l12.grid(row=3, column=1)
        rld = DoubleVar()
        rld.set(.5)
        Label(l12, text="right lane : ", bg='white', anchor=E).grid(row=0, column=0, sticky="nsew")
        Entry(l12, textvariable=rld, width=5, bg='whitesmoke').grid(row=0, column=1)

        lld = DoubleVar()
        lld.set(.5)
        Label(l12, text="left lane : ", bg='white', anchor=E).grid(row=1, column=0, sticky="nsew")
        Entry(l12, textvariable=lld, width=5, bg='whitesmoke').grid(row=1, column=1)

        Label(l1, text="number of obstacles : ", bg='white', anchor=E).grid(row=4, column=0, sticky="nsew")
        l13 = Frame(l1, bg='white')
        l13.grid(row=4, column=1)

        rlnOb = DoubleVar()
        rlnOb.set(5)
        Label(l13, text="right lane : ", bg='white', anchor=E).grid(row=0, column=0, sticky="nsew")
        Entry(l13, textvariable=rlnOb, width=5, bg='whitesmoke').grid(row=0, column=1)

        llnOb = DoubleVar()
        llnOb.set(5)
        Label(l13, text="left lane : ", bg='white', anchor=E).grid(row=1, column=0, sticky="nsew")
        Entry(l13, textvariable=llnOb, width=5, bg='whitesmoke').grid(row=1, column=1)

        ########################

        def register():

            self.lp = (lp.get() == 1)
            self.angle = angle.get()*np.pi/180 #degrees to angles
            self.u_d = 0.514444*u_d.get()
            self.rlw = rlw.get()
            self.llw = llw.get()
            self.ld = ld.get()
            self.dAsv = 10.
            self.ll = max(self.rlw+self.llw+self.ld,
                          200+(self.ld+self.llw+self.llw+self.dAsv)/np.tan(self.angle))

            if dORn.get() == 0:
                self.rld = rld.get()/10000
                self.lld = lld.get()/10000
                self.rlnOb = int(self.rld*self.rlw*self.ll)
                self.llnOb = int(self.lld*self.llw*self.ll)
            else:
                self.rlnOb = int(rlnOb.get())
                self.llnOb = int(llnOb.get())
                self.rld = self.rlnOb/self.rlw/self.ll
                self.lld = self.llnOb/self.llw/self.ll

            #fenetre.destroy()
            self.opus += 1

            self.write_input()

            self.run()
            try:
                if self.opus == 1 :
                    global f
                    f = open(self.output, "r")
                    content = f.readline().rstrip('\n')
                    Label(second_frame, text=content, anchor=NW, bg='white').pack(fill="x")

                content = f.readline().rstrip('\n')
                Label(second_frame, text=content, anchor=NW, bg='white').pack(fill="x")
            except FileNotFoundError:
                self.opus-=1
                #clear input
                pass

            update_plot()


        bouton=Button(first_frame, text="Start Simulation",
                      command=register,
                      bd=6, width=15, height=2)
        bouton.config(font=('Batang', 35))
        bouton.grid(row=2, column=1)

        ########################
        ########################

        graph_frame = Frame(aux_frame, width=w_small, height=2*h_unit, bg='whitesmoke')
        graph_frame.pack(fill='both', expand='yes')
        Label(graph_frame, text='No data', bg='whitesmoke', anchor=CENTER).pack(fill='both', pady=h_unit-10)

        #fig = plot_graph(0, 2, w_small/100, 2*h_unit/100)
        #chart_type = FigureCanvasTkAgg(fig, aux_frame)
        #graph = chart_type.get_tk_widget().pack()


        f1 = Frame(aux_frame, bg='gainsboro')
        f2 = Frame(aux_frame, bg='gainsboro')
        f1.pack(side=LEFT, expand='yes')
        f2.pack(side=LEFT, expand='yes')
        Label(f1, text='X :', bg='gainsboro').pack()
        Label(f2, text='Y :', bg='gainsboro').pack()

        x = IntVar()
        y = IntVar()
        x_list = [["Opus",0], ["ASV Speed",1], ["Obstacle Heading",3]]
        y_list = [["Natural Collision Indic.",2], ["Logarithmic Collision Indic.",1], ["Anticipation Indic.",4]]
        x.set(0)
        y.set(2)

        def update_plot():
            if self.opus >= 1:
                clear_frame(graph_frame)
                fig = self.plot_graph(x.get(), y.get(), w_small/100, 2*h_unit/100)
                #FigureCanvasTkAgg(fig, aux_frame).get_tk_widget().pack()
                chart_type = FigureCanvasTkAgg(fig, graph_frame)
                chart_type.get_tk_widget().pack()

        for w in x_list:
            Radiobutton(f1, variable=x, text=w[0], value=w[1], bg='gainsboro', anchor=W, highlightthickness=0, command=update_plot).pack(fill='both')
        for w in y_list:
            Radiobutton(f2, variable=y, text=w[0], value=w[1], bg='gainsboro', anchor=W, highlightthickness=0, command=update_plot).pack(fill='both')

        ########################
        ########################
        fenetre.mainloop()
        try:
            f.close()
        except NameError:
            pass
        ########################

    def write_input(self):

        param = [self.opus,
                 self.angle,
                 self.u_d,
                 self.rlnOb,
                 self.llnOb,
                 self.rlw,
                 self.llw,
                 self.ld,
                 self.ll,
                 self.rld,
                 self.lld,
                 0]

        f = open(self.input,'a')

        if self.opus == 1:
            f.write(f'OPUS    ANGLE    U_D    RLNOB    LLNOB    RLW    LLW    LD    LL     RLD    LLD    GP\n')
        for p in param:
            f.write(f'{p}    ')
        f.write('\n')
        f.close()

        print('=====================================')
        print('local planner : ', self.lp)
        print('angle : ', self.angle)
        print('u_d : ', self.u_d)
        print('right lane density : ', self.rld)
        print('left lane density : ', self.lld)
        print('=====================================')

    def run(self):
        # ASV parameters
        initial_state_asv = [-(self.ld/2+self.llw+self.dAsv)/np.tan(self.angle),-(self.ld/2+self.llw+self.dAsv),self.angle, self.u_d,0.,0.]
        #Trajectory
        waypoints_asv = [[-(self.ld/2+self.llw+self.dAsv)/np.tan(self.angle),-(self.ld/2+self.llw+self.dAsv)],
                         [(self.ld/2+self.rlw+self.dAsv)/np.tan(self.angle),self.ld/2+self.rlw+self.dAsv]]

        # Creation of the launch files
        cli_args0 = ['cross_lane', 'crossLane.launch',
                     f'rlnOb:={self.rlnOb}',
                     f'llnOb:={self.llnOb}',
                     f'rlw:={self.rlw}',
                     f'llw:={self.llw}',
                     f'ld:={self.ld}',
                     f'll:={self.ll}',
                     f'trigger_shutdown:=0',
                     f'initial_state:={initial_state_asv}',
                     f'waypoints:={waypoints_asv}',
                     f'u_d:={self.u_d}',
                     f'use_vo:={self.lp}',
                     f'rviz:=true',
                     f'opus:={self.opus}',
                     f'output_file:=$(find cross_lane)/output/{serial}.txt',
                     f'pos_end_waypoint:={waypoints_asv[-1]}']
        roslaunch_file0 = roslaunch.rlutil.resolve_launch_arguments(cli_args0)[0]
        roslaunch_args0 = cli_args0[2:]
        launch_files = [(roslaunch_file0, roslaunch_args0)]

        launch = roslaunch.parent.ROSLaunchParent(uuid, launch_files)
        launch.start()
        launch.spin()

    def plot_graph(self, i, j, width, height):

        x = []
        y = []
        xlab = ['OPUS', 'ANGLE', 'U_D', 'RLD', 'LLD', 'RLW', 'LLW', 'LD', 'GP']
        ylab = ['LOG_COL', 'NAT_COL', 'OFFSET_LOG', 'ANTICIPATION']
        labels = []
        colors = []
        f1 = open(self.input,'r')
        f2 = open(self.output,'r')
        f1.readline()
        f2.readline()

        for line in f1:
            content = line.split()
            x.append(float(content[i]))
            labels.append('Velocity Obstacles' if content[2] == "True" else 'No LP')
            colors.append('orange' if content[2] == "True" else 'blue')
        for line in f2:
            content = line.split()
            y.append(float(content[j]))
        f1.close()
        f2.close()

        figure = plt.Figure(figsize=(width,height), dpi=100)

        ax = figure.add_subplot(111)
        ax.set_title("Results of the Simulation")
        ax.set_xlabel(xlab[i])
        ax.set_ylabel(ylab[j-1])

        for p in range(1,len(x)):
            ax.plot(x[p], y[p], 'o', color=colors[p], label=labels[p])

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())

        return figure


if __name__ == "__main__":

    # Output parameters
    now = datetime.datetime.now()
    serial = now.strftime("%Y%m%d%H%M%S")[2:]
    # UUID
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)

    scenar = Scenario(serial, 0, uuid)

    scenar.graphic_interface()

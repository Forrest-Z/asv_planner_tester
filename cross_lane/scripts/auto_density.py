#!/usr/bin/env python3

import roslaunch
import numpy as np
import datetime
import rospkg

NB_PROCESS = 5
OPUS_START = 1
NOBMIN = 4
NOBMAX = 8
NB_REP = 15
SERIAL_TO_UPDATE = 'density6'

def run(serial, params, uuid) :

    rospack = rospkg.RosPack()
    first_opus = params[0][0]

    cli_args0 = ['asv_referee', 'reaper.launch',
                 f'nb_processes:={NB_PROCESS}',
                 f'opus:={first_opus}']
    roslaunch_file0 = roslaunch.rlutil.resolve_launch_arguments(cli_args0)[0]
    roslaunch_args0 = cli_args0[2:]
    launch_files = [(roslaunch_file0, roslaunch_args0)]

    lp = True

    for scenar in params:

        opus = scenar[0]
        angle = np.pi/2      #degrees to radians
        u_d = 0.514444*15    #knots to m/s
        llnOb = scenar[1]
        rlnOb = scenar[1]
        rlw = 400.       #m
        llw = 400.       #m
        ld = 200         #m
        gp = 0
        ll = rlw+llw+ld

        rld = rlnOb/rlw/ll            #right lane obstacle density in 1/m²
        lld = llnOb/llw/ll            #left lane obstacle density in 1/m²

        # ASV parameters
        dAsv = 100. #initial and final distance to lanes
        initial_state_asv = [-(ld/2+llw+dAsv)/np.tan(angle),-(ld/2+llw+dAsv),angle, u_d,0.,0.]
        #Trajectory
        waypoints_asv = [[-(ld/2+llw+dAsv)/np.tan(angle),-(ld/2+llw+dAsv)],
                         [(ld/2+rlw+dAsv)/np.tan(angle),ld/2+rlw+dAsv]]

        input = f"{rospack.get_path('cross_lane')}/input/{serial}.txt"
        f = open(input,'a')
        par = [opus,
                 angle,
                 u_d,
                 rlnOb,
                 llnOb,
                 rlw,
                 llw,
                 ld,
                 ll,
                 rld,
                 lld,
                 0]
        for p in par:
            f.write(f'{p}    ')
        f.write(f'\n')
        f.close()

        # Creation of the launch files
        cli_args1 = ['cross_lane', 'crossLane.launch',
                     f'rlnOb:={rlnOb}',
                     f'llnOb:={llnOb}',
                     f'rlw:={rlw}',
                     f'llw:={llw}',
                     f'ld:={ld}',
                     f'll:={ll}',
                     f'trigger_shutdown:=0',
                     f'initial_state:={initial_state_asv}',
                     f'waypoints:={waypoints_asv}',
                     f'u_d:={u_d}',
                     f'use_vo:={lp}',
                     f'rviz:=False',
                     f'opus:={opus}',
                     f'output_file:=$(find cross_lane)/output/{serial}.txt',
                     f'pos_end_waypoint:={waypoints_asv[-1]}']
        roslaunch_file1 = roslaunch.rlutil.resolve_launch_arguments(cli_args1)[0]
        roslaunch_args1 = cli_args1[2:]
        launch_files.append((roslaunch_file1, roslaunch_args1))
        #print([opus, angle, u_d, nOb, rlw, llw, ld])
    launch = roslaunch.parent.ROSLaunchParent(uuid, launch_files)
    launch.start()
    launch.spin()


if __name__ == "__main__":
    rospack = rospkg.RosPack()

    # UUID
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    # Output parameters
    if len(SERIAL_TO_UPDATE) == 0: 
        now = datetime.datetime.now()
        serial = now.strftime("%Y%m%d%H%M%S")[2:]
    else:
        serial = SERIAL_TO_UPDATE

    # Write Input
    input = f"{rospack.get_path('cross_lane')}/input/{serial}.txt"
    f = open(input,'a')
    f.write(f'OPUS    ANGLE    U_D    RLNOB    LLNOB    RLW    LLW    LD    LL     RLD    LLD    GP\n')
    f.close()

    opus = 1
    count = 0
    params = []

    try:
        for lnOb in range(NOBMIN,NOBMAX):
            for rep in range(NB_REP):
                params.append([opus, lnOb])
                if len(params) == NB_PROCESS:
                    run(serial, params, uuid)
                    params = [] 
                opus += 1
            # except:
            #     print("Unexpected error:", sys.exc_info()[0])
            #     output = f"{rospack.get_path('cross_lane')}/output/{serial}.txt"
            #     g = open(input,'a')
            #     g.write(f'{opus+1} nan nan nan nan nan nan nan nan nan nan nan nan nan\n')
            #     g.close()
            #     params = []
    except KeyboardInterrupt:
        pass

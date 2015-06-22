#!/usr/bin/env python
"""
  ___________________________________________________
 |  _____                       _____ _ _       _    |
 | |  __ \                     |  __ (_) |     | |   |
 | | |__) |__ _ __   __ _ _   _| |__) || | ___ | |_  |
 | |  ___/ _ \ '_ \ / _` | | | |  ___/ | |/ _ \| __| |
 | | |  |  __/ | | | (_| | |_| | |   | | | (_) | |_  |
 | |_|   \___|_| |_|\__, |\__,_|_|   |_|_|\___/ \__| |
 |                   __/ |                           |
 |  GNU/Linux based |___/  Multi-Rotor UAV Autopilot |
 |___________________________________________________|
  
 Rotation Position Control

 Copyright (C) 2015 Tobias Simon, Integrated Communication Systems Group, TU Ilmenau

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details. """


from scl import scl_get_socket, SCL_Reader
from msgpack import dumps, loads
from time import sleep
import traceback

# setpoint readers:
sp_p = SCL_Reader('rp_ctrl_sp_p', 'sub')
sp_r = SCL_Reader('rp_ctrl_sp_r', 'sub')

# enable readers:
p_oe = SCL_Reader('rp_ctrl_p_oe', 'pull')
p_oe.data = 1 # enabled, if nothing received
r_oe = SCL_Reader('rp_ctrl_r_oe', 'pull')
r_oe.data = 1 # enabled, if nothing received

# outgoing sockets:
spp_p_socket = scl_get_socket('rs_ctrl_spp_p', 'push')
spp_r_socket = scl_get_socket('rs_ctrl_spp_r', 'push')

orientation_socket = scl_get_socket('orientation', 'sub')
try:
   while True:
      yaw, pitch, roll = loads(orientation_socket.recv())

      kp = 6.0
      pitch_err = pitch - sp_p.data
      if p_oe.data:
         spp_p_socket.send(dumps(-pitch_err * kp))

      roll_err = roll - sp_r.data
      if r_oe.data:
         spp_r_socket.send(dumps(-roll_err * kp))

      #print rp_ctrl_sp_p.data, rp_ctrl_sp_r.data, pitch, roll, pitch_err, roll_err
except Exception as e:
   print traceback.format_exc()


## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import sys
import math
import argparse
import struct
import enum
import os
import pathlib
import socket
import openocd
import shutil

serial ='N2GEA1601C0001'
KM=0

def word2bytes(word):
 result=[(word)&0xff,(word>>8)&0xff,(word>>16)&0xff,(word>>24)&0xff]
 return bytes(result)
 
if __name__ == '__main__':
 oocd = openocd.OpenOcd('localhost', 6666)

 try:
  oocd.connect()
 except Exception as e:
  sys.exit('Failed to connect to OpenOCD')
 shutil.copy('data.bin','data_temp.bin')
 scooter_data=open('data_temp.bin','r+b')
 # Disable RDP
 sys.stdout.write('unsecuring device...\n')
 sys.stdout.flush()
 oocd.send('init')
 oocd.send('reset halt')
 oocd.send('stm32f1x unlock 0')
 oocd.send('reset')
 sys.stdout.write('done\n')
 # read UUID
 oocd.send('init')
 oocd.send('reset halt')
 sys.stdout.write('reading UUID\n')
 sys.stdout.flush()
 UUID = oocd.read_memory(0x1FFFF7E8,3)
 output_value = 'done: %08x %08x %08x\n' % (UUID[0],UUID[1],UUID[2])
 sys.stdout.write(output_value)
 sys.stdout.write('preparing sooter data...\n')
 sys.stdout.flush()
 scooter_data.seek(0x20)
 scooter_data.write(serial.encode())
 scooter_data.seek(0x1b4)
 scooter_data.write(word2bytes(UUID[0]))
 scooter_data.seek(0x1b8)
 scooter_data.write(word2bytes(UUID[1]))
 scooter_data.seek(0x1bc)
 scooter_data.write(word2bytes(UUID[2]))
 scooter_data.seek(0x52)
 scooter_data.write(word2bytes(KM*1000))
 scooter_data.close()
 sys.stdout.write('flashing...\n')
 sys.stdout.flush()
 oocd.write_binary(0x08000000,'es2_boot.bin')
 oocd.write_binary(0x08001000,'es2_firm.bin')
 oocd.write_binary(0x0801c000,'data_temp.bin')
 sys.stdout.write('done\n')

 UUID2 = oocd.read_memory(0x0800F9B4,3)
 output_value = '%08x %08x %08x\n' % (UUID2[0],UUID2[1],UUID2[2])
 sys.stdout.write(output_value)
 
 sys.stdout.write('done\n')
 sys.stdout.flush()
 input("Press Enter to continue...")

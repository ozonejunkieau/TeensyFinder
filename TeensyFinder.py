# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:53:44 2019

@author: Tristan Steele

This is a helper function to ease the process of connecting to Teensy devices.
"""

import serial.tools.list_ports


class TeensyFinder:
    
    #Default list of VID, PID that count as a teensy.
    DEFAULT_ID_LIST = [
            (0x16C0, 0x0483),
            ]
    
    def __init__(self, auto_search = True):
        """Set's up a TeensyFinder instance, using default PID/VID values."""
        self.id_list = TeensyFinder.DEFAULT_ID_LIST
        self.sp_list = None
        
        if auto_search:
            self.find_all_teensy()   
        
    def add_vid_pid(self, vid, pid):
        """Simply add other VID, PID values that may be useful."""
        self.id_list.append((int(vid), int(pid)))
        
        #Reset the serial port list, as the results may now be different
        self.sp_list = None
    
    def find_all_teensy(self):
        """Search for all devices that match the criteria."""
        
        all_ports = serial.tools.list_ports.comports()
        
        self.sp_list = [sp for sp in all_ports if (sp.vid, sp.pid) in self.id_list]
        
        self.sp_count = len(self.sp_list)
    
    def get_the_teensy(self, serial_suffix = None):
        """An optimistic function for getting the serial port of a Teensy.
        If no serial_suffix is provided, and only one Teensy is found, it is 
        returned.
        
        The serial suffix ignores the trailing zero used in Teensy serial 
        numbers."""
        
        if self.sp_list is None:
            self.find_all_teensy()

        if serial_suffix is None or serial_suffix == "":           
            if self.sp_count == 0:
                raise Exception("No Teensy devices found.")    
            elif len(self.sp_list) == 1:
                return self.sp_list[0]    
            else:
                raise Exception("Multiple Teensy devices found.") 
        else:
            serial_suffix_str = str(serial_suffix)
            
            matching_devices = []
            match_len = len(serial_suffix_str)
            
            for sp in self.sp_list:
                this_device_serial = str(sp.serial_number[:-1])
                
                if this_device_serial[-match_len:] == serial_suffix_str:
                    matching_devices.append(sp)
                    
            if len(matching_devices) == 1:
                return matching_devices[0]
            elif len(matching_devices) == 0:
                raise Exception("No Teensy device found with that serial.")  
            else:
                raise Exception("Multiple Teensy devices found with that serial.")  
        
    def __repr__(self):
        """Print something pretty"""
        
        if self.sp_list is None:
            return "TeensyFinder: No search has been run."
        else:
            return "\n".join(["{0}:- {1}".format(sp.description, sp.hwid) for sp in self.sp_list])
        
    def __str__(self):
        """Print the same thing pretty."""
        return self.__repr__()


## Some basic demonstration code that prints a list of found Teensy devices.
if __name__ == "__main__":
    tf = TeensyFinder()
    print(tf)

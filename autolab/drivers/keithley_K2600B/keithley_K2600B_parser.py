#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import keithley_K2600B as MODULE
from argparse import ArgumentParser


class Driver_parser():
    def __init__(self,args,utilities,**kwargs):
        self.utilities = utilities
        """Set the connection up"""
        self.classes_list = self.utilities.list_classes(MODULE)
        Driver_class      = self.utilities.identify_device_class(MODULE,self.classes_list,args.link)
        self.Instance     = Driver_class(address=args.address,**kwargs)
        
        self.methods_list = self.utilities.list_methods(self.Instance)
        
        
    def add_parser_arguments(self,parser):
        """Add arguments and help to the parser passed as input"""
        usage = f"""
----------------  Driver informations:  ----------------
{self.help()}

----------------  Examples:  ----------------

usage:    autolab-drivers [options] arg 
            
    autolab-drivers -d {MODULE.__name__} -i GPIB::7::INSTR -l VISA -v 0.2 -c A,B
    load {MODULE.__name__} driver using VISA communication protocol with address TCPIP... and set the voltage to 0.2V to channel A and B
    
    autolab-drivers -d nickname -v 0.2 -c A
    same as before but using the device nickname as defined in devices_index.ini
    
    autolab-drivers -d nickname -m some_methods1,arg1,arg2=23 some_methods2,arg1='test'
    Execute some_methods of the driver. A list of available methods is present at the top of this help along with arguments definition.
            """
        parser = ArgumentParser(usage=usage,parents=[parser])
        parser.add_argument("-c", "--channels", type=str, dest="channels", default=None, help="Set the channels to act on." )
        parser.add_argument("-v", "--voltage", type=str, dest="voltage", default=None, help="Set the current in mA." )
        
        return parser

    def do_something(self,args):
        if args.channels:
            for chan in args.channels.split(','):
                if args.voltage:
                    getattr(getattr(self.Instance,f'channel{chan}'),'setVoltage')(args.voltage)
            
        if args.methods:
            methods = [args.methods[i].split(',') for i in range(len(args.methods))]
            message = self.utilities.parse_commands(self.Instance,methods,self.methods_list)

    def help(self):
        """Add to the help lists of module: classes, methods and arguments"""
        classes_list = self.utilities.print_help_classes(self.classes_list)                  # display list of classes in module
        methods_list = self.utilities.print_help_methods(self.methods_list)                  # display list of methods in module
        methods_args = self.utilities.print_help_methods_arguments(self.Instance,self.methods_list)      # display list of methods arguments
        return classes_list + methods_list + methods_args

    def exit(self):
        #I.close()
        sys.exit()

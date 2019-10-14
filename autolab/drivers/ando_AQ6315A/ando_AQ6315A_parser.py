#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import agilent_MXAN9020A as MODULE
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
        
    autolab-drivers -d {MODULE.__name__} -i TCPIP::192.168.0.3::INSTR -l VISA -o my_output_file -c A
    Results in saving one file for the trace A, the data as seen on the scope
    
    autolab-drivers -d nickname -o my_output_file -c A B C
    Same as previous one but with 3 output files on per trace (A, B and C) and using the device nickname as defined in devices_index.ini
            """
        parser = ArgumentParser(usage=usage,parents=[parser])
        parser.add_argument("-c", "--channels", nargs='+', type=str, dest="channels", default=None, help="Set the traces to act on/acquire from." )
        parser.add_argument("-o", "--filename", type=str, dest="filename", default='DEFAULT', help="Set the name of the output file" )
        parser.add_argument("-F", "--force",action="store_true", dest="force", default=None, help="Allows overwriting file" )
        #parser.add_argument("-t", "--trigger", type=str, dest="trigger",action="store_true", help="Trigger the scope once" )
        
        return parser

    def help(self):
        """Add to the help lists of module: classes, methods and arguments"""
        classes_list = self.utilities.print_help_classes(self.classes_list)                  # display list of classes in module
        methods_list = self.utilities.print_help_methods(self.methods_list)                  # display list of methods in module
        methods_args = self.utilities.print_help_methods_arguments(self.Instance,self.methods_list)      # display list of methods arguments
        return classes_list + methods_list + methods_args

    def do_something(self,args):
        if args.filename:
            #getattr(self.Instance,'get_data_traces')(traces=args.channels,single=args.trigger)
            getattr(self.Instance,'get_data_traces')(traces=args.channels)
            getattr(self.Instance,'save_data_traces')(filename=args.filename,traces=args.channels,FORCE=args.FORCE)
  
        if args.methods:
            methods = [args.methods[i].split(',') for i in range(len(args.methods))]
            message = self.utilities.parse_commands(self.Instance,methods,self.methods_list)


    def exit(self):
        self.Instance.close()
        sys.exit()

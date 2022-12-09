import os
import sys
import argparse
import json
import re

global DEBUG
global MAIN_DIR
global PROJ_DIR

DEBUG = "Off"
MAIN_DIR = os.path.dirname(sys.argv[0])
PROJ_DIR = os.path.abspath(os.path.join(MAIN_DIR,os.pardir))

class CompileCommands(object):

    sSearch = "# Compiling source file"
    dataLocation = 2
    symbolToStripFromLeft = "["
    symbolToStripFromRight = "]"

    def __init__(self,LOG_FILE,COMPILE_COMMANDS) -> None:
        self.LOG_FILE = LOG_FILE
        self.COMPILE_COMMANDS = COMPILE_COMMANDS

    def __call__(self) -> None:
        LOG_DATA = self.readLogFile()
        self.compileCommands(LOG_DATA)

        if DEBUG == "On":
            compile_commands_data = self.parse_tree(LOG_DATA)
            print(compile_commands_data)

        print(f"::set-output name=init::{True}")

    def readLogFile(self) -> map:
        
        c_files = {}
        with open(self.LOG_FILE, 'r+', encoding="utf-8") as file:
            lines = file.readlines()
            for i in range(0, len(lines)):
                # Strip newlines from right (trailing newlines)
                line = lines[i]
                if line.startswith(self.sSearch) and (i < len(lines)-2):
                    compilation = lines[i+self.dataLocation]
                    c_files[line] = compilation

        return c_files

    def parse_tree(self,map) -> map:

        return map

    def compileCommands(self,map) -> None:
        pattern = re.compile("\[(.*?)\]") # Matches everything between [] brackets
        with open(self.COMPILE_COMMANDS, 'w+', encoding='utf-8') as json_file:
            final_array = []
            for compiledFile,options in map.items():
                match = pattern.search(compiledFile)
                c_file=match.group(0).split('/')[-1].rstrip(self.symbolToStripFromRight)
                c_path=match.group(0).lstrip(self.symbolToStripFromLeft).rstrip(self.symbolToStripFromRight)
                c_path=c_path.replace("/"+c_file,"")
                arguments = options.split("\n")[0]
                new_map = {}
                new_map["directory"] = c_path
                new_map["command"] = arguments
                new_map["file"] = c_file
                final_array.append(new_map)
            json_file.write(json.dumps(final_array, indent = 4, sort_keys=False))
            json_file.close()

        return

def main():

    try:
        if (len(sys.argv) > 1):
            parser = argparse.ArgumentParser(description='Process Log File.')
            parser.add_argument('--log', '-l', type=str, help='The path the log file')
            parser.add_argument('--output', '-o', type=str, help='The path to the output compile commands file')
            parser.add_argument('--config', '-c', type=str, help='The config folder name located in main folder')
            args = parser.parse_args()
            config_folder = args.config
            log_file = args.log
            output_file = args.output
        else:
            config_folder = "config"
            log_file = "build.log"
            output_file = "compile_commands.json"

        CONFIG_DIR = os.path.join(PROJ_DIR,config_folder)
        LOG_FILE = os.path.join(CONFIG_DIR,log_file)
        OUTPUT_FILE = os.path.join(CONFIG_DIR,output_file)
        compileCommandsInit = CompileCommands(LOG_FILE,OUTPUT_FILE)
        compileCommandsInit()

    except Exception as e:
        raise Exception(f'Catching Exception error {e}')


if __name__ == "__main__":
    main()

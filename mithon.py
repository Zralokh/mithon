"""The main file of the mithon project

   This is called whenever mithon is invoked via command line

   Mithon aims to increase your productivity of writing minecraft ingame code by
   wrapping the functionality and exposing more easy to use, higher level functionality.
"""
import click
from typing import *
from pathlib import Path
from packaging import version
Version = version.Version


import pkg_resources
this:Dict[str, Any] = {}
this.update({"version":pkg_resources.require("mithon")[0].version})

from .app.minecraft import MCVersion


acceptedMC: List[MCVersion] = [MCVersion.JE]
acceptedJEVersions:List[Version]
acceptedBEVersions:List[Version]
acceptedMCVersions: Tuple(List[Version]) = (acceptedJEVersions, acceptedBEVersions)
MCVersionRange: Tuple[Tuple[Version]] = (
   (acceptedVersions[0],
    acceptedVersions[-1]) 
   for acceptedVersions in acceptedMCVersions)

def printAvailableVersions()->str:
   return " and ".join(
          str(
             (str(mctype)+
              " "+
              "-".join(str(MCVersionRange[mctype]).split(','))
             ) for mctype in acceptedMC
          ).split(',')
       )

#TODO add github link to description
project_description=f"""
   Mithon  Copyright (C) 2023  Zralokh (github.io/...)
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
    
    This program currently only supports {printAvailableVersions()}
"""

defaultDir:Path = r"%appdata%/.minecraft/datapacks/mithon"
defaultName:str = "MyMithonProject"
defaultVersion: Version = version.parse("0.0.1")
defaultMC: MCVersion = MCVersion.JE
defaultMCVersion: Version = version.parse("1.19.4")



def print_version(ctx, param, value):
   if not value or ctx.resilient_parsing:
      return
   click.echo('Version 1.0')
   ctx.exit()
   
   
@click.group()
@click.command()
@click.option('-v', '--version', is_flag=True, expose_value=False, is_eager=True, callback=print_version)
def cli():
   pass

@cli.command()
@click.option('-d', '--directory', 'dir', 
              type=str, 
              default=defaultDir, 
              help='the directory where to build into')
@click.option('-n', '--name', 
              type=str, 
              default=defaultName, 
              prompt='Your project\'s name',
              help='the name of the project')
@click.option('-v', '--version', 
              type=str, 
              default=defaultVersion, 
              help='the version of your datapack')
@click.option('-mcv', '--mc-version',
              type=str, 
              default=defaultMCVersion, 
              prompt='',
              help='Minecraft version to transpile to')
@click.option('-s', '--strict', 'preserve',
              type=bool, 
              is_flag=True,
              default=False, 
              help='preserve variable- and function-names')
#TODO implement the linking to the app module and do the stuff there
#TODO implement error messages
def build(dir: Path=defaultDir, name:str=defaultName, version:str=defaultVersion, preserve:bool=False):
   """
   """
   click.echo(project_description)
   click.echo(f"Building")


#TODO implement hot reload, build only the new changes
@cli.command()
def serve():
   """Hot-Reload: if invoked, the tool stays awake and awaits file changes and builds them into your datapack directly

   serve is a hot reload functionality, that enables you to test in minecraft as you code. Make sure to type /reload whenever you made changes. This version of building is not optimized and may sometimes break something as it only transpiles the changes you made on the code. For a complete optimized build, use 'mithon build' instead.
   """
   
   
   click.echo("""
      serve is a hot reload functionality, that enables you to test in minecraft as you code. Make sure to type /reload whenever you made changes. 
      This version of building is not optimized and may sometimes break something as it only transpiles the changes you made on the code. For a complete optimized build, use 'mithon build' instead.
      """
   )


@cli.command()
@click.option('-w', '--warranty', 
              type=bool, 
              is_flag=True,
              help="Show the detailed warranty", 
              default=False)
@click.option('-c', '--copyright', 
              type=bool, 
              is_flag=True,
              help="Show the detailed copyright", 
              default=False)
@click.option('-f', '--full', 
              type=bool, 
              is_flag=True,
              help="Show the entire license", 
              default=False)
@click.option('-v', '--versions',
              type=bool, 
              is_flag=True,
              help="Show the supported MC versions", 
              default=False)
def show(warranty, copyright, full, versions):
   if warranty:
      with open("./LICENSE") as file:
         while(file.readline().find("15.") == -1):
            pass
         lines = file.readline()
         click.echo("  15. Disclaimer of Warranty.  \n")
         while(lines.find("16.") == -1):
            click.echo(lines)
            lines = file.readline()
            
   if copyright:
      with open("./LICENSE") as file:
         while(file.readline().find("2.") == -1):
            pass
         lines = file.readline()
         click.echo("  2. Basic Permissions.  \n")
         while(lines.find("3.") == -1):
            click.echo(lines)
            lines = file.readline()
            
   if warranty or copyright:
      click.echo("\nTo see the full license with all its terms type 'show -f or --full'.")
            
   if full:
      with open("./LICENSE") as file:
         for lines in file.readlines():
            click.echo(lines)
   
   if versions:
      click.echo(printAvailableVersions())


#TODO implement linking to app
def main(*args, **kwargs):
   """The mithon main function if mithon is called as a python package instead, also the entry point for direct invocation
   """
   pass

if __name__ == "__main__":
   import sys
   main(sys.argv)
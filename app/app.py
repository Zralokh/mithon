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
Directory = NewType("Directory", Path)

import pkg_resources
this:Dict[str, Any] = {}
this.update({"version":pkg_resources.require("mithon")[0].version})

from .minecraft import MCVersion

#handling MC version stuff
acceptedMC: List[MCVersion] = [MCVersion.JE]
acceptedJEVersions:List[str] = ["1.19.4"]
acceptedBEVersions:List[str] = []
acceptedMCVersions: List[List[Version]] = [[version.parse(v) for v in acceptedJEVersions], [version.parse(v) for v in acceptedBEVersions]]
MCVersionRange: List[List[Version]] = [
   [acceptedVersions[0],
    acceptedVersions[-1]] 
   for acceptedVersions in acceptedMCVersions if len(acceptedVersions)>0]

availableVersions:str = " and ".join(
                     str(
                        [mctype.name+" "+
                           ("-".join(
                              str(
                                 [str(v) for v in MCVersionRange[mctype.int]]
                              ).split(', '))
                           ) for mctype in acceptedMC]
                     ).split(', ')
                  ).replace("'", "").replace("[","").replace("]","")

#TODO add github link to description
project_description=f"""
   Mithon  Copyright (C) 2023  Zralokh (github.com/Zralokh/mithon)
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
    
    This program currently only supports {str(availableVersions)}
"""

defaultDir:Path = r"%appdata%/.minecraft/datapacks/mithon"
defaultName:str = "MyMithonProject"
defaultVersion: Version = "0.0.1"
defaultMC: MCVersion = MCVersion.JE
defaultMCVersion: Version = "1.19.4"



def print_version(ctx, param, value):
   """Shows the version of mithon"""
   if not value or ctx.resilient_parsing:
      return
   click.echo('Version 1.0')
   ctx.exit()
   
   
@click.group()
@click.version_option(version=this["version"])
def cli():
   click.echo("Hi it seems you are using mithon. If you like it, please share word <3")
   click.echo(project_description)

@cli.command()
@click.option('-d', '--directory', 'dir', 
              type=click.Path(), 
              default=defaultDir, 
              help=f'the output directory [{defaultDir}]')
@click.option('-n', '--name',
              type=str, 
              default=defaultName, 
              prompt='Your project\'s name',
              help=f'the name of the project [{defaultName}]')
@click.option('-v', '--version', 'version_',
              type=str, 
              default=defaultVersion, 
              help=f'the version of your datapack [{defaultVersion}]')
@click.option('-mcv', '--mc-version',
              type=str, 
              default=defaultMCVersion, 
              prompt=f'Minecraft Version',
              help=f'minecraft version to transpile to [{defaultMCVersion}]')
@click.option('--java/--bedrock', '-JE/-BE', 
              default=("JE"==defaultMC.str),
              help=f'Java Edition or Bedrock Edition [{defaultMC.str}]')
@click.option('-s', '--strict', 'preserve',
              type=bool, 
              is_flag=True,
              default=False, 
              help='preserve variable- and function-names [false]')
@click.argument('target', type=click.Path())
#TODO implement the linking to the app module and do the stuff there
#TODO implement error messages
def build(target: str, dir: Path=defaultDir, name:str=defaultName, version_:str=defaultVersion, mc_version:str=defaultMCVersion, java:bool=True, preserve:bool=False):
   """builds TARGET into a datapack with optimized code\n
   
   build is the production build functionality. It builds your datapack from the ground up thus aullowing for much greater optimization.
   
   Args:\n
      target(str): directory to build from
   """
   if not name.lower().isalpha:
      raise ValueError("name has to alpha only")
   
   #TODO change if bedrock is supported
   if not java:
      raise ValueError("this project only supports "+availableVersions)
   
   #mc_version is a valid version, not checked if this 
   mc_version = version.parse(mc_version)
   if not (mc_version >= MCVersionRange[1-java][0] and mc_version <= MCVersionRange[1-java][1]):
      raise ValueError(f"mc version is not allowed, has be to one of ({availableVersions}) [not the JE, BE tag, see build --help]")
   
   
   
   #check if version is a valid version
   try:
      version_ = version.parse(version_)
   except:
      raise ValueError("version is not a valid version")
   
   
   
   click.echo(f"Building {name}-{version_} for MC version {mc_version} out of {target} to {dir}. Preserving names={preserve}.")


#TODO implement hot reload, build only the new changes
@cli.command()
@click.argument('target', type=click.Path())
def serve():
   """Hot-Reload: builds changes in TARGET directly\n

   serve is a hot reload functionality, that enables you to test in minecraft as you code. Make sure to type /reload whenever you made changes. This version of building is not optimized and may sometimes break something as it only transpiles the changes you made on the code. For a complete optimized build, use 'mithon build' instead.
   
   Args:\n
      target(str): directory to build from
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
   """shows helpful information
   """
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
      click.echo(availableVersions+"\n")
      
   if not (warranty or copyright or full or versions):
      click.echo("Type 'mithon show --help' to see how to use mithon show.")

if __name__ == "__main__":
   cli()
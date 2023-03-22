"""The main file of the mithon project

   This is called whenever mithon is invoked via command line

   Mithon aims to increase your productivity of writing minecraft ingame code by
   wrapping the functionality and exposing more easy to use, higher level functionality.
"""
from app.app import cli

if __name__ == "__main__":
   cli()
   
   
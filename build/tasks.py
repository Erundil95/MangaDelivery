from invoke import task
import os

@task
def build(c):
    # Build executable
    c.run("pyinstaller ..\\main.spec")
    # move config file into executable folder
    c.run("python copy_config.py")
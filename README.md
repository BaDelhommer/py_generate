# py_generate

## First personal project for Boot.dev

### This will remain a work in progress, use at your own risk.

This is a Python script for creating a generate.go file to bundle resources for a fyne app

Prompts the user to select the path to the directory that contains the resources to be bundled ex: "./my_resources". It then prompts the user to select the path for the generate.go file ex: "./generate.go". It will then create a generate.go file at the specified location that contains the //go:generate commamds to bundle resources for a fyne app. Helpful for bundling many resources.

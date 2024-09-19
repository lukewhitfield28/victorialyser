# victorialyser

A portmanteau of "Victoria 2" and "Analyser".

![victorialyser screenshot](https://i.imgur.com/2k6yEOt.png)

Inspired by [VickyWarAnalyzer](https://github.com/TKasekamp/VickyWarAnalyzer), this Victoria 2 save game analyser provides a modern method of reading war data from your playthroughs as you might during an AAR. Like he who inspired the project, this began as a learning opportunity but has developed into a workable project with further development planned.

# Requirements
## Python 3
### Windows
For the best experience, please install Python 3 through the [official website](https://www.python.org/downloads/). 

Otherwise, please use the Windows Store.

### Linux
Python 3 is likely already installed. If not, install it using your preferred package manager.

# Installation
## Releases
Go to the latest release, then download the file associated with your operating system. Extract the file, then run the executable within to use the application.

## pipx
The pipx project allows you to easily install the application in an isolated virtual environment, adding victorialyser to your $PATH for ease of use. 

If pipx is not already installed on your system, please install it using the instructions found on the [official GitHub repository](https://github.com/pypa/pipx).

Once installed, these commands can be used as a guide on how to install and run victorialyser:
#### Clone victorialyser
```bash
git clone https://github.com/lukewhitfield28/victorialyser.git
```

#### Change directory into the cloned folder
```bash
cd victorialyser
```

#### Install victorialyser
```bash
pipx install --include-deps .
```

#### The result of the previous command may recommend you run this to add victorialyser to $PATH
```bash
pipx ensurepath
```

#### Finally, you can call victorialyser from your command line or terminal:
```bash
victorialyser
```

These are loose instructions. For example, you may have to call pipx directly by finding where the executable is installed. You can also create your own virtual environment, or run the scripts in a variety of other ways per your discretion. If you need help, please don't hesitate to ask and I'll aim to help you as soon as possible.

# Usage
On first launch, you will first be prompted to select the folder containing your Victoria 2 installation. This folder is almost certainly called Victoria 2 and found in a directory such as "../steam/steamapps/common/Victoria 2." 

Afterwards, you will be prompted to select a save game file. Any "*.v2" file is valid. 

The analyser will now load, with the option to change both these settings found in the bottom-right.

# Future Development
## Mod Support
There's currently implicit mod support. Any modded file should load, but with missing information. This will vary from missing graphics, localisation, or missing figures from unaccounted unit types. I intend to add full mod support in the future.

## Statistics
Certain data points are currently excluded, for example war goals, as they aren't collated very well in the save files. I do intend on presenting this data in the future, along with niche yet valuable information such as province terrain modifiers. This would naturally coincide with pulling data through modded files.

## Suggestions
Any and all feedback is appreciated. I will periodically update this page when appropriate.
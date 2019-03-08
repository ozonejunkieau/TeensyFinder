# TeensyFinder

This helper function is designed to ease the pain of working with Teensy devices. Devices can be queried by serial number, giving a unique identifier to communicate with a project instead of the mess that USB Serial Ports can become.

It's a quick little thing, it hasn't been exhaustively tested but should throw errors when you try and do silly things.

## Installation
`pip install git+https://github.com/ozonejunkieau/TeensyFinder.git`


## Usage
```
from TeensyFinder import TeensyFinder
tf = TeensyFinder()

# Display a list of all found devices.
print(tf)
> USB Serial Device (COM10):- USB VID:PID=16C0:0483 SER=xxxxx40 LOCATION=1-6
> USB Serial Device (COM11):- USB VID:PID=16C0:0483 SER=xxxxx60 LOCATION=1-5

# Return types are pySerial ListPortInfo, so to get a com port reference:
tf.get_the_teensy('4').device
> 'COM1'

# If only a single Teensy is detected, it will return that device if no query:
tf.get_the_teensy().device
> 'COM1'

# If a custom VID, PID is required to be used for matching:
tf.add_vid_pid(vid_as_int, pid_as_int)
# Search again given the update to the valid devices, which should happen automatically.
tf.find_all_teensy()
```


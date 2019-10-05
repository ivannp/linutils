# linutils
Utilities to handle lin movies (BridgeBase's file format)

# Creating html for BridgeBase hands
The files need to be downloaded manually [from BridgeBase](www.bridgebase.com/myhands/). A few example files are stored in the session directory.

    python htmlize.py -o html\output.html session\*
    
Running the above command generates html\output.html, which contains the boards.

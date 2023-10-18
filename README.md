# DLL-Spoofer 
This python script scans a provided DLL's exports and creates a basic duplicate CPP DLL template. All exported functions are re-used and pop a simple message window. 
Additionally on DLL attach we execute the first exported function. This is useful for simple providing POC for DLL hijacking since we're not duping function arguements. 

This can easily be used to execute shellcode generated via msfvenom. Just replace the first function in the output template. 


# Usage

``` python3 spoof.py
usage: spoof.py [-h] dll_path

Generate a C++ source file for a DLL that displays MessageBox for exported functions.

positional arguments:
  dll_path    Path to the DLL to inspect and create the C++ source for.

optional arguments:
  -h, --help  show this help message and exit

```

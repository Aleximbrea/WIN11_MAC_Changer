# MAC Spoofer for Windows

Simple python script that changes registry keys to change mac adresses of network interfaces

## Usage

To use the script you need a python installation, i used version *3.11.10*, you also need **administrator privileges**

1. Clone the repository:
    ```bash
    git clone https://github.com/Aleximbrea/WIN11_MAC_Changer.git
    ```

2. Navigate to the project folder

3. Open the command prompt and run:
    ```bash
    python main.py
    ```

## How it works

- It executes the following commands to gather information about your current network interfaces:
      ```
      netsh interface show interface
      ```
      ```
      getmac -v
      ```
  - View your network interfaces so you can choose the one you want to modify
  - Then it disables it, changes the registry key **NetworkAddress** and re-enables the interface
 
  ## Notes

  - Some interfaces have special rules for mac adresses so the changes might not work
  - You need admin privileges
  - Leave blank the new MAC field if you want one to generate one automatically
  

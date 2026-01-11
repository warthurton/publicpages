# Change Network Type in Windows 10/11 (Private/Public)

Run the following PowerShell command:

	Get-NetConnectionProfile
	
See the network name you want to change its type and run the following command: 

	Set-NetConnectionProfile -Name “NetworkName” -NetworkCategory Public
	
NetworkCategory switch value to `Public` or `Private`.
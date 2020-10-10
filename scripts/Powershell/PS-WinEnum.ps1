echo "THE DATE FOR THIS SYSTEM IS:"
get-date
echo ""
echo "THE SYSTEM CONFIGURATION IS:"; 
get-Ciminstance win32_OperatingSystem | FL *
echo "THE USER IS:"
Get-WmiObject -class win32_computersystem | select username | FL
echo "OPEN CONNECTIONS:"
Get-NetTCPConnection | FT
echo "OPEN FILES (Requires Admin):"
openfiles /query | FL
echo "PROCESSES:"
Get-Process | FT
echo "DLLs:"
Get-Process | select  -ExpandProperty modules | sort-object modulename | Get-Unique | select modulename | FL
echo "MAPPED DRIVES:"
Get-PSDrive | select name, description
echo ""
echo "CONFIGURED DEVICES:"
Get-WmiObject win32_pnpsigneddriver | select devicename | FL
echo ""; echo "SHARED RESOURCES:" ; echo ""
get-wmiobject -class win32_share
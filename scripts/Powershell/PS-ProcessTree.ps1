#pull process list as a collection of objects
$ProcessList = get-wmiobject win32_process | select name, parentprocessid, processid
cls
#define function Get-Child
Function Get-Child($global:UpdatedList, $Process, $D)
{
	foreach($P in $global:UpdatedList)
		{
		if($P.ParentProcessID -eq $Process.ProcessID)
			{
				$name=$P.name
				$PPID=$P.ParentProcessID
				$PIDs=$P.ProcessID
				echo "$D $name $PPID $PIDs"
				
				$global:UpdatedList = ($global:UpdatedList | where{$_.processid -ne $PIDs})
				$DD = $D + "--"
				Get-Child $global:UpdatedList $P $DD
				
			}
		}
}


#remove processes where processid = 0 (root) to prevent infinite loop
$global:UpdatedList = ($ProcessList | where{$_.processid -ne 0})

#Prints the 1ST Process to avoid infinite Loop
$PP = $ProcessList | where{$_.processid -eq 0}
echo $PP
#depth variable visually shows nested families
$Depth = "--"

#Iterate first only
Get-Child $global:UpdatedList $PP $Depth
echo ""



foreach($Process in $global:UpdatedList)
{
	foreach($Check in $global:UpdatedList)#Deals with scoping issue of the list
	{
		if($Check -eq $Process)
		{
			echo $Process
			#Updates list to take out current process
			$global:UpdatedList = ($global:UpdatedList | where{$_.processid -ne $Process.Processid})
			Get-Child $global:UpdatedList $Process $Depth
			echo ""
		}
	}
}
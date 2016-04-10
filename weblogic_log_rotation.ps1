### weblogic_log_rotation on windows machienes using powershell 
### the script logic is 
### find .out files which size is more than 500 MB and modified today then copy its content to another log file of this day and make it empty 

$date=Get-Date -UFormat "%Y-%m-%d-%H-%M"
### C:\test is an arbitrary directory you can modify it according to your needs 
$large_out_files=get-childitem c:\test\ -include *.out -recurse | Where-Object { $_.LastWriteTime -gt (get-date).AddDays(-1) -and $_.length -gt 524288000 } | Sort-Object length |% { $_.FullName } 

foreach ( $large_file in $large_out_files ) 
{ 
	echo $($large_file+"_"+$date)
	cp $large_file $($large_file+"_"+$date) 
	Clear-Content $large_file
}

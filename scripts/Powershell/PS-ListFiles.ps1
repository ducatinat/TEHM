echo "The date for the open files is:"
get-date
echo ""
echo "Here are the open files:"
D:\CYBER\"SysInternals Suite"\handle | select-string "File" | select Line |  Sort-Object Line | ForEach{$_.Line.SubString(21)}  |Sort-Object | gu -asstring 
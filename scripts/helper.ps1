Set-Location -Path "C:\Users\marco\blender-text-to-speech-offline"
$Src = "Text to Speech"
$Zipped = "Text to Speech.zip"
if (Test-Path $Zipped) 
{
  Remove-Item $Zipped
  Compress-Archive -Path $Src -DestinationPath $Zipped
}
else
{
	Compress-Archive -Path $Src -DestinationPath $Zipped
}
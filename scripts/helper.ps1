$Src = "text_to_speech"
$Zipped = "text_to_speech.zip"
$Addon = "C:\Users\mlaga\AppData\Roaming\Blender Foundation\Blender\3.5\scripts\addons"

Set-Location -Path "C:\Users\mlaga\code\blender-text-to-speech"

if (Test-Path $Zipped) 
{
  Remove-Item $Zipped
  Compress-Archive -Path $Src -DestinationPath $Zipped
}
else
{
	Compress-Archive -Path $Src -DestinationPath $Zipped
}

if (Test-Path $Addon)
{
  Remove-Item -Recurse $Addon
}
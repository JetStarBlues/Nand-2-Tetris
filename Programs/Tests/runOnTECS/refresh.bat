@echo off

rem Note: unlike typing directly, script will not ask before overwritting


set dstPath="...\runOnTECS"

set program_srcPath="...\gav\GASscroller\*.vm"

set os_srcPath="...\precompiledOS\*.vm"


echo Removing existing VM files...
del *.vm

echo Copying new VM files...

rem Copy OS VM files
copy %os_srcPath% %dstPath%

rem Copy program VM files
copy %program_srcPath% %dstPath%

echo Done!

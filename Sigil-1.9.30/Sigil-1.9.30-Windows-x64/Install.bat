@Echo Off

Reg.exe add "HKLM\SOFTWARE\Classes\.epub\OpenWithList\Sigil.exe" /f
Reg.exe add "HKLM\SOFTWARE\Classes\.epub\OpenWithProgids" /v "SigilEPUB" /t REG_SZ /d "" /f
Reg.exe add "HKLM\SOFTWARE\Classes\.htm\OpenWithList\Sigil.exe" /f
Reg.exe add "HKLM\SOFTWARE\Classes\.html\OpenWithList\Sigil.exe" /f
Reg.exe add "HKLM\SOFTWARE\Classes\.xhtml\OpenWithList\Sigil.exe" /f
Reg.exe add "HKLM\SOFTWARE\Classes\Applications\Sigil.exe" /v "FriendlyAppName" /t REG_SZ /d "Sigil: a cross-platform EPUB editor" /f
Reg.exe add "HKLM\SOFTWARE\Classes\Applications\Sigil.exe\DefaultIcon" /ve /t REG_SZ /d "%~dp0Sigil.exe,0" /f
Reg.exe add "HKLM\SOFTWARE\Classes\Applications\Sigil.exe\shell\open\command" /ve /t REG_SZ /d "\"%~dp0Sigil.exe\" \"%%1\"" /f
Reg.exe add "HKLM\SOFTWARE\Classes\Applications\Sigil.exe\SupportedTypes" /v ".epub" /t REG_SZ /d "" /f
Reg.exe add "HKLM\SOFTWARE\Classes\SigilEPUB" /ve /t REG_SZ /d "EPUB" /f
Reg.exe add "HKLM\SOFTWARE\Classes\SigilEPUB\DefaultIcon" /ve /t REG_SZ /d "%~dp0Sigil.exe,0" /f
Reg.exe add "HKLM\SOFTWARE\Classes\SigilEPUB\shell\open\command" /ve /t REG_SZ /d "\"%~dp0Sigil.exe\" \"%%1\"" /f
::����ע���

Reg.exe add "HKCR\SigilEPUB" /ve /t REG_SZ /d "EPUB" /f
Reg.exe add "HKCR\SigilEPUB\DefaultIcon" /ve /t REG_SZ /d "%~dp0Sigil.exe,0" /f
Reg.exe add "HKCR\SigilEPUB\shell\open\command" /ve /t REG_SZ /d "\"%~dp0Sigil.exe\" \"%%1\"" /f
::����ע���ROOT

xcopy  "%~dp0Package Cache" "C:\ProgramData\Package Cache" /c /e /h /y
echo Starting Microsoft Visual C++ 2015-2019 Redistributable (x64) -14.26.28808...
PowerShell -Command "start 'C:\ProgramData\Package Cache\{78079cc3-1f6e-47f6-b4d6-105f08b89409}\VC_redist.x64.exe'"
::���Ʋ���װMicrosoft Visual C++���п�

echo �Ƿ�����ɫ�������ļ������أ�(y/n)
set /p judge=
if "%judge%" == "y"  goto yes
if "%judge%" == "n"  goto no

:yes
xcopy  "%~dp0sigil-ebook" "C:\Users\%username%\AppData\Local\sigil-ebook" /c /e /h /y
::������ɫ�������ļ�������

:no
Exit

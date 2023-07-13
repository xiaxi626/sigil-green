@Echo Off

Reg.exe delete "HKLM\SOFTWARE\Classes\.epub\OpenWithList\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\.epub\OpenWithProgids" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\.htm\OpenWithList\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\.html\OpenWithList\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\.xhtml\OpenWithList\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\Applications\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\SigilEPUB" /f
::删除注册表
Reg.exe delete "HKCR\SigilEPUB" /f
::删除注册表ROOT


PowerShell -Command "start 'C:\ProgramData\Package Cache\{78079cc3-1f6e-47f6-b4d6-105f08b89409}\VC_redist.x64.exe'"
::运行Microsoft Visual C++运行库卸载程序
pause

echo 是否复制配置文件到绿色版？(y/n)
set /p judge=
if "%judge%" == "y"  goto yes
if "%judge%" == "n"  goto no
:yes
xcopy  "%LocalAppData%\sigil-ebook" "%~dp0sigil-ebook" /c /e /h /y
::复制配置文件到绿色版
goto OUTFOR

:no
goto OUTFOR

:OUTFOR
rd /s /q "%LocalAppData%\sigil-ebook" 
del "%SystemRoot%\Prefetch\SIGIL.EXE-**" /a /f /q
del "%SystemRoot%\Prefetch\SIGIL-**" /a /f /q
del "%SystemRoot%\Prefetch\QTWEBENGINEPROCESS.EXE-**" /a /f /q
::删除配置文件和Prefetch预读取文件

Exit

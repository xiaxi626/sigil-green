@Echo Off

Reg.exe delete "HKLM\SOFTWARE\Classes\.epub\OpenWithList\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\.epub\OpenWithProgids" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\.htm\OpenWithList\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\.html\OpenWithList\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\.xhtml\OpenWithList\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\Applications\Sigil.exe" /f
Reg.exe delete "HKLM\SOFTWARE\Classes\SigilEPUB" /f
::ɾ��ע���
Reg.exe delete "HKCR\SigilEPUB" /f
::ɾ��ע���ROOT


PowerShell -Command "start 'C:\ProgramData\Package Cache\{12410e80-cba2-4479-8539-12de3513ff53}\VC_redist.x86.exe'"
::����Microsoft Visual C++���п�ж�س���
pause

echo �Ƿ��������ļ�����ɫ�棿(y/n)
set /p judge=
if "%judge%" == "y"  goto yes
if "%judge%" == "n"  goto no
:yes
xcopy  "C:\Users\%username%\AppData\Local\sigil-ebook" "%~dp0sigil-ebook" /c /e /h /y
::���������ļ�����ɫ��
goto OUTFOR

:no
goto OUTFOR

:OUTFOR
rd /s /q "C:\Users\%username%\AppData\Local\sigil-ebook" 
del "%SystemRoot%\Prefetch\SIGIL.EXE-**" /a /f /q
del "%SystemRoot%\Prefetch\SIGIL-**" /a /f /q
del "%SystemRoot%\Prefetch\QTWEBENGINEPROCESS.EXE-**" /a /f /q
::ɾ�������ļ���PrefetchԤ��ȡ�ļ�

Exit

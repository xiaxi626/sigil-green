@Echo Off

echo �Ƿ�װ��������ļ������أ�(y/n)
set /p judge=
if "%judge%" == "y"  goto yes
:yes
xcopy  "%~dp0plugin\plugins" "C:\Users\%username%\AppData\Local\sigil-ebook\sigil\plugins" /c /e /h /y
xcopy  "%~dp0plugin\plugins_prefs" "C:\Users\%username%\AppData\Local\sigil-ebook\sigil\plugins_prefs" /c /e /h /y
::������ɫ���������ļ�������

:no
Exit
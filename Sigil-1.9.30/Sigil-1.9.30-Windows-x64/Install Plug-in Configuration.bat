@Echo Off

echo 是否安装插件配置文件到本地？(y/n)
set /p judge=
if "%judge%" == "y"  goto yes
:yes
xcopy  "%~dp0plugin\plugins" "C:\Users\%username%\AppData\Local\sigil-ebook\sigil\plugins" /c /e /h /y
xcopy  "%~dp0plugin\plugins_prefs" "C:\Users\%username%\AppData\Local\sigil-ebook\sigil\plugins_prefs" /c /e /h /y
::复制绿色版插件配置文件到本地

:no
Exit
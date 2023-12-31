分章助手使用说明：

1、关于“正则表达式”：
　　表达式建议都添加句首符号“^”和句尾符号“$”，避免误杀正文内容。
　　正则表达式输入框可以留空，留空或输入纯空白字符，则不起任何作用。
　　表达式为Python正则语法，可以通过Sigil或Notepad++先测试正则效果。

2、关于“标题级别”：
　　标题级别可选值为1-6，设置后插件会将匹配到的内容对应标题级别套上 h1~h6标签。

３、关于“分割”：
　　分割”选项作用是决定搜索到的标题是否进行分章。
　　如果不勾选，则仅仅会套上h1-h6标签，但不会分割到独立页面。

4、关于“预览”：
　　预览功能可以预先查看插件分章的效果，开始执行前建议进行预览一下。
　　如果预览不显示任何内容，说明插件无法在TXT中匹配到任何标题。
　　【双击】标题项可删除该处标题，一旦标题的匹配表达式改变，则删除标题设置将失效。

5、关于工具栏 “+”，“-”，“笔”：
　　“+”：添加正则搜索框，最多添加到15个。
　　“-”：减少正则搜索框。
　　“笔”：编辑预置正则表达式

6、关于“修改模板”：
　　模板是一个xhtml页面文件的模板，它的本质是一段xhtml代码，用[MAIN]变量和[TITLE]变量指定内容位置。
      [MAIN] 变量指定了标题（带h1-h6标签）和正文内容的位置。
      [TITLE] 变量是一段没有标签的标题文段，一般放在<title>元素中，也可根据需求改变位置。
      其中 [MAIN] 只能有一个，[TITLE] 变量可以指定多个。

7、文件命名规则：
　　文件命名一般为 “英文前缀”+“数字序号”，例如“Chapter0001”。
　　“数字序号”决定了起始文件名的序号，后续的文件名序号将在该序号基础上递增。
　　“数字序号”的有效数字前面可以加“0”表示占用宽度，例如“001”表示该数字宽度至少为3位，则该序号序列将为001、002、……、099、100……

8、 关于“自动分析”：
　　插件可自定分析标题，自动分析的原理是——逐个尝试预置正则，一旦正则能匹配到内容则添加入正则框。
　　虽然插件真正在执行过程中【可防止】重复匹配，但在自动分析过程是【没有防止】重复匹配的，
　　【因此自动分析有可能添加入多个匹配效果相同的表达式】
　　因插件执行中可防止重复匹配，所以就算用了多个效果相同的表达式，
　　也不会影响最终效果，只是仍会微略影响插件运行效率。
　　如果介意，手动清空不需要的正则框内容即可。

★9、 关于“表达式的执行顺序”及“防止重复匹配”：

　　表达式的执行顺序是按正则框位置【由上到下】，
　　由于插件有进行【防止重复匹配】的措施，
　　因此【下一个表达式】一般是无法匹配到【上一个表达式】已经匹配到的内容。
　　（因为插件的防重复匹配措施比较简单，仅仅是匹配到的内容马上套上对应的h1~h6标签，
　　　因此特殊写法，例如不带＾和＄符号的表达式，或带h1~h6标签的表达式有可能重复匹配）

　　利用这一特性，对含有相似内容的标题进行分级具有一定作用，
　　例如下面这种标题：
　　#####################
　　第二卷  翻云覆雨
　　第二卷  第1章  诬陷
　　第二卷  第2章  夺刀
　　#####################
　　如果你期望“第二卷 翻云覆雨”设为一级标题，“第二卷 第N章”设为二级标题。
　　若你先搜索 【^第.卷.*$】，则可能把“第二卷 第N章”也误设为一级标题。
　　可以先搜索【^第.卷 第.章.*$】，再搜索【^第.卷.*$"】，就能达到你的期望。

10、关于断序检查：
　　在预览中开启“断序检查”，插件将提取标题中含有的第一串“中文数字”或“阿拉伯数字”字符串，
　　并转化为可比较的数字类型。如果前一章到后一章的数字值增加一，则标题呈现绿色，否则呈现警戒颜色。
      支持【两千零二】、【二〇〇二】、【2002】、【２００２】之类的数字字符串。
　　注意：【不同级别】的标题是处于【不同比对组】，警戒颜色也不同。
                 若把“第一卷”、“第一章”之类的标题设为不同级别，则其数值不会相互干扰。
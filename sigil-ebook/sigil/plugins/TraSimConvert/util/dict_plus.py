# -*- coding: utf-8 -*-

#自定义映射表注意：
#
#  决定映射优先度的首先是关键词长度，其次是关键词在书写中的排序前后：当长度不同时，关键词长度越长，优先度越高。当关键词相同时，书写顺序越靠后优先度越高。
#  例如一个关键词“龍捲風”，其映射优先度肯定大于关键词“龍捲”，因為“龍捲風”长度比“龍捲”长一个字符。
#  这意味着文本中如果存在“龍捲風”的词汇，程序将优先以“龍捲風”的映射替换文本，而不是先以“龍捲”的映射替换文本，再以“風”的映射替换文本。
#  当映射字典中存在两个以上相同的关键词时，程序将以书写排序靠后的关键词映射表为准，写在后面的映射会覆盖前面的映射。
#  这意味着当你书写某个映射时，如果不确定前面有没有写过，往后面写就对了。
#

#繁转简
tra_to_sim = {
'著':'着',
'著作':'著作',
'名著':'名著',
"著名":"著名",
'专著':'专著',
"土著":"土著",
"巨著":"巨著",
"昭著":"昭著",
"显著":"显著",
"卓著":"卓著",
"知著":"知著",
"欲盖弥著":"欲盖弥著",
'簷': '檐',
'飮': '饮',
'痩': '瘦',
'呪': '咒',
'傚': '效',
'讬': '托',
'壊': '坏',
'砲': '炮',
'拚': '拼',
'揹': '背',
'搥': '捶',
'姊': '姐',
'䙓': '摆',
'蒐羅': '搜罗',
'蒐罗': '搜罗',
'蒐集': '搜集',
'高䠷': '高挑',
'保镳': '保镖',
'搆到': '够到',
'锻鍊': '锻炼',
'鍊金': '炼金',
'铁鍊': '铁链',
'项鍊': '项链',
'百鍊': '百炼',
'弹鍊': '弹链',
'夹鍊袋': '夹炼袋'
}

#简转繁
sim_to_tra = {
'着':'著'
}
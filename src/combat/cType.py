from eudplib import *
from eudplib.core.eudfunc.consttype import createEncoder
from eudplib.core.rawtrigger.strenc import _EncodeAny
import helpers.fx
import re
import customText4 as ct

actionDict = [
    "(None)", "이동", "공격", "도주",
    "물기", "할퀴기", "냥냥펀치",
]

skillDict = []
expireDict = [
    "일반", "차례", "액션"
]

buffList = [  # 버프는 배열도 만들어야하니 특별 취급.
    "\x1C방어"
]
buffN = len(buffList)

skillList = [
    "\x08펀치",  # 일반공격
    "\x1F물기", "\x08할퀴기", "\x1B냥냥펀치",  # rhoddl
]
skillDict.extend(buffList)  # 버프를 앞에, 스킬을 뒤에 위치시킨다.
skillDict.extend(skillList)

skillName = EUDArray([Db(u2utf8(x)) for x in skillDict])
skillIGA = EUDArray([Db(u2utf8(helpers.fx.IGA(x))) for x in skillDict])
skillEUL = EUDArray([Db(u2utf8(helpers.fx.EUL(x))) for x in skillDict])
skillURO = EUDArray([Db(u2utf8(helpers.fx.URO(x))) for x in skillDict])

combatMsgDict = [
    "(None)", "criticalHit"
]
actionDict = {k: v for v, k in enumerate(actionDict)}
expireDict = {k: v for v, k in enumerate(expireDict)}
skillDict = {k: v for v, k in enumerate(skillDict)}
combatMsgDict = {k: v for v, k in enumerate(combatMsgDict)}


def f_skill(txt):
    txt = unProxy(txt)
    try:
        return skillDict[txt]
    except KeyError:
        for s, i in skillDict.items():
            if re.search(txt, s) is not None:
                return i
        raise KeyError


def EncodeSkill(txt, issueError=True):
    return _EncodeAny("SkillName", f_skill, skillDict, txt, issueError)


def f_expire(txt):
    txt = unProxy(txt)
    return expireDict[txt]


def EncodeExpire(txt, issueError=True):
    return _EncodeAny("BuffExpireType", f_expire, expireDict, txt, issueError)


Skill = createEncoder(EncodeSkill)
Expire = createEncoder(EncodeExpire)


def f_combatMsg(txt):
    txt = unProxy(txt)
    return combatMsgDict[txt]


def EncodeCombatMsg(txt, issueError=True):
    return _EncodeAny("CombatMsg", f_combatMsg, combatMsgDict, txt, issueError)


CombatMsg = createEncoder(EncodeCombatMsg)


def f_action(txt):
    txt = unProxy(txt)
    return actionDict[txt]


def EncodeAction(txt, issueError=True):
    return _EncodeAny("CombatAction", f_action, actionDict, txt, issueError)


Action = createEncoder(EncodeAction)


def f_strSkill(txt):
    return ct.f_str(skillName[f_skill(txt)])

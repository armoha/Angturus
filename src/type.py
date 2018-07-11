from eudplib import *
from eudplib.core.eudfunc.consttype import createEncoder
from eudplib.core.rawtrigger.strenc import _EncodeAny


DefAngDict = {
    # (".*"): ([0-9]+,) -> [\1]=\2
    "F.A.H": 7,
    "Elemental": 34,
    "AceRPG": 79,
    "Fare.": 51,
    "YOU": 61,  # Dark Templar
    "YOU2": 315,  # Civilian
    "goddess": 16,
}
DefChatDict = {
    # "(.*)": ([0-9]+), -> \1: \2
    "스킵!": 2,
    "skip!": 2,
    "소개": 3,
    "introduction": 3,
    "이름": 3,
    "name": 3,
    "ㅎㅇ": 3,
    "hi": 3,
    "소문": 4,
    "gossip": 4,
    "대화": 4,
    "talk": 4,
    "스킬": 5,
    "skill": 5,
    "기술": 5,
    "거래": 6,
    "trade": 6,
    "안녕": 7,
    "bye": 7,
    "ㅂㅇ": 7,
}


def Ang(ass):
    ass = unProxy(ass)
    return DefAngDict[ass]


def EncodeAngString(ass, issueError=True):
    return _EncodeAny("AngString", Ang, DefAngDict, ass, issueError)


def Chat(txt):
    txt = unProxy(txt)
    return DefChatDict[txt]


def EncodeChatText(txt, issueError=True):
    return _EncodeAny("ChatText", Chat, DefChatDict, txt, issueError)


AngString = createEncoder(EncodeAngString)
ChatText = createEncoder(EncodeChatText)

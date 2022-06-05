from eudplib import *
import customText4 as ct
import struct


def _IGVA(vList, exprListGen):
    def _():
        exprList = exprListGen()
        SetVariables(vList, exprList)

    EUDOnStart(_)


centerX = EUDCreateVariables(1)
_IGVA([centerX], lambda: [320])

conNext = [Forward() for _ in range(2)]


@EUDFunc
def f_mouseover(x, y, width, height):
    if EUDIf()(
        EUDSCAnd()(Memory(0x6CDDC4, AtLeast, x))(Memory(0x6CDDC4, AtMost, x + width))(
            Memory(0x6CDDC8, AtLeast, y)
        )(Memory(0x6CDDC8, AtMost, y + height))()
    ):
        EUDReturn(1)
    if EUDElse()():
        EUDReturn(0)
    EUDEndIf()


@EUDFunc  # fx.mouseover(420, 170, 250, 50)
def f_mouseoverNext():
    if EUDIf()(
        EUDSCAnd()(conNext[0] << Memory(0x6CDDC4, AtLeast, 1))(
            conNext[1] << Memory(0x6CDDC4, AtMost, 2)
        )(Memory(0x6CDDC8, AtLeast, 170))(Memory(0x6CDDC8, AtMost, 220))()
    ):
        EUDReturn(1)
    if EUDElse()():
        EUDReturn(0)
    EUDEndIf()


@EUDFunc
def f_setpcolor(pnum, color):
    pcolor_dst = 0x581D76 + 8 * pnum
    mcolor_dst = 0x581DD6 + pnum
    f_bwrite(pcolor_dst, color)
    f_bwrite(mcolor_dst, color)


@EUDTypedFunc([TrgLocation])
def f_getLocationX(loc):
    locTable = EPD(0x58DC60)
    EUDReturn(
        (f_dwread_epd(locTable + loc * 5) + f_dwread_epd(locTable + loc * 5 + 2)) // 2
    )


@EUDTypedFunc([TrgLocation])
def f_cView(loc):
    oldcp = f_getcurpl()
    f_setcurpl(f_getuserplayerid())
    DoActions(CenterView(loc))
    locX = f_getLocationX(loc - 1)
    screenX = f_dwread_epd_safe(EPD(0x628448))
    centerX << (locX - screenX)
    DoActions(
        [
            SetMemory(conNext[0] + 8, SetTo, centerX * 3 // 2 - 90),
            SetMemory(conNext[1] + 8, SetTo, centerX * 3 // 2 + 90),
        ]
    )
    f_setcurpl(oldcp)


@EUDFunc
def f_getDstSquare(x1, x2, y1, y2):
    dx, dy = List2Assignable([x1 - x2, y1 - y2])
    EUDReturn(dx * dx + dy * dy)


@EUDFunc
def f_setUnitColor(epd, colorp):
    oldcp = f_getcurpl()
    f_setcurpl(f_epdread_epd(epd + 0xC // 4) + 2)
    b2 = f_bread_cp(0, 2)
    DoActions(
        [
            SetDeaths(CurrentPlayer, Subtract, b2, 0),
            SetDeaths(CurrentPlayer, Add, colorp * 0x10000, 0),
        ]
    )
    f_setcurpl(oldcp)


def Jongsung(s):
    c1, c2, c3 = struct.unpack("<ccc", s[-1].encode("UTF-8"))
    c1 = b2i1(c1) - 0b11100000
    c2 = b2i1(c2) - 0b10000000
    c3 = b2i1(c3) - 0b10000000
    s = 4096 * c1 + 64 * c2 + c3
    return (s - 0xAC00) % 28


def IGA(s):
    if Jongsung(s) == 0:
        return "가"
    else:
        return "이"


def EUL(s):
    if Jongsung(s) == 0:
        return "를"
    else:
        return "을"


def EUN(s):
    if Jongsung(s) == 0:
        return "는"
    else:
        return "은"


def URO(s):
    if Jongsung(s) == 0 or Jongsung(s) == 8:  # ㄹ
        return "로"
    else:
        return "으로"


@EUDFunc
def Rand(maxv):
    EUDReturn(f_rand() % maxv)


@EUDFunc
def HotkeyUnit(epd, player, hotkey, slot):
    targetOrderSpecial = f_dwread_epd(epd + 0xA5 // 4) & 0xFF00
    alphaID = EUDVariable()
    if EUDIf()(epd == 19025):
        alphaID << 1 + targetOrderSpecial * 8
    if EUDElse()():
        alphaID << 1701 - (0x27821 - epd) // 0x54 + targetOrderSpecial * 8
    EUDEndIf()
    f_dwwrite_epd(EPD(0x57FE60) + 216 * player + 12 * hotkey + slot, alphaID)


@EUDFunc
def ABS(x):
    if EUDIf()(x >= 0x80000000):
        EUDReturn(-x)
    if EUDElse()():
        EUDReturn(x)
    EUDEndIf()


@EUDTypedFunc([TrgPlayer, TrgModifier, None, TrgUnit])
def SetKills(Player, Modifier, Number, Unit):
    DoActions([SetMemoryEPD(EPD(0x5878A4) + 12 * Unit + Player, Modifier, Number)])


@EUDTypedFunc([TrgUnit])
def f_getLeastKills(unit):
    for p in EUDLoopRange(8):
        f_setcurpl(p)
        if EUDIf()(LeastKills(unit)):
            EUDReturn(p)
        EUDEndIf()


@EUDTypedFunc([TrgUnit])
def f_getMostKills(unit):
    for p in EUDLoopRange(8):
        f_setcurpl(p)
        if EUDIf()(MostKills(unit)):
            EUDReturn(p)
        EUDEndIf()


@EUDFunc
def f_getNextUnit():
    return f_dwepdread_epd(EPD(0x628438))


def SetEnemyName(txt, name, iga, eun, eul, uro):
    f_dbstr_print(name, txt)
    f_dbstr_print(iga, IGA(txt))
    f_dbstr_print(eun, EUN(txt))
    f_dbstr_print(eul, EUL(txt))
    f_dbstr_print(uro, URO(txt))


def internalDiv(a, b, i, maxv):
    return int(round((i * b + (maxv - i) * a) / maxv))


@EUDFunc
def MakeR():  # Make whitespace relative to screen width
    default = 33
    maxDif = 18  # 최대 28개 차이나게
    if EUDIf()(centerX <= internalDiv(320, 426, 1, maxDif + 1)):
        ct.f_makeText(" " * default)
    for i in range(2, maxDif + 1):
        if EUDElseIf()(centerX <= internalDiv(320, 426, i, maxDif + 1)):
            ct.f_makeText(" " * (default + i - 1))
    if EUDElse()():
        ct.f_makeText(" " * (default + maxDif))
    EUDEndIf()


def DisplayR(player, *args):
    MakeR()
    ct.f_addText(*args)
    ct.f_displayTextP(player)

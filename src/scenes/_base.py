from eudplib import *
import customText4 as ct
import helpers.timeline as tL


# sBuffer = ct._CGFW(lambda: [GetStringIndex("z" * 600)], 1)[0]
# txtLines = EUDVariable()


def f_procString(*args):  # processString
    args = FlattenList(args)
    txtList, txtLen = [], 0
    color = ""
    for arg in args:
        try:
            len(arg.encode("UTF-8"))
        except (AttributeError, TypeError):
            txtList.extend([arg])
            txtLen += 12
        else:
            string = ""
            for c in arg:
                c_utf8 = c.encode("UTF-8")
                c_b2i = ct.b2i(c_utf8)
                if (c_b2i >= 0x01 and c_b2i <= 0x1F and
                        c_b2i != 0x12 and c_b2i != 0x13):
                    color = c
                    continue
                string += color + c
                for i in range(3 - len(c_utf8)):
                    string += "\x0D"
            string += color
            txtList.extend([string])
            txtLen += len(string.encode("UTF-8"))
    return txtList, txtLen


def f_initTimer(index):
    tL.v[index] << 0


"""def f_talk(*args, interval=1):
    ret = EUDVariable()
    txtList, txtlen = f_procString(*args)
    # ct.f_reset_epd()
    ct.f_makeText_epd(*txtList)
    ct.f_reset()
    for t in tL.Timeless(txtlen // 4, interval):
        if EUDIf()(t == txtlen // 4 - 1):
            ret << 1
        if EUDElse()():
            ret << 0
            f_bwrite_epd(ct.epd + t, 3, 0x14)
        EUDEndIf()
    DoActions(DisplayText(ct.strBuffer))
    return ret"""


def f_fadeIn(*args, interval=1, index=0):
    ret = EUDVariable()
    txtList, txtlen = f_procString(*args)
    # ct.f_reset_epd()
    ct.f_makeText_epd(*txtList)
    ct.f_reset()
    for t in tL.Timeless(txtlen // 4 + 3, interval, index):
        if EUDIf()(t == txtlen // 4 + 2):
            ret << 1
        if EUDElse()():
            ret << 0
            if EUDIf()(t >= 3):
                f_bwrite_epd(ct.epd + t - 3, 3, 0x03)
            EUDEndIf()
            if EUDIf()([t >= 2, t <= txtlen // 4 + 1]):
                f_bwrite_epd(ct.epd + t - 2, 3, 0x04)
            EUDEndIf()
            if EUDIf()([t >= 1, t <= txtlen // 4]):
                f_bwrite_epd(ct.epd + t - 1, 3, 0x05)
            EUDEndIf()
            if EUDIf()(t <= txtlen // 4 - 1):
                f_bwrite_epd(ct.epd + t, 3, 0x14)
            EUDEndIf()
        EUDEndIf()
    DoActions(DisplayText(ct.strBuffer))
    return ret


def f_talk(*args, interval=1, index=0):
    ret = EUDVariable()
    txtList, txtlen = f_procString(*args)
    # ct.f_reset_epd()
    ct.f_makeText_epd(*txtList)
    ct.f_reset()
    for t in tL.Timeless(txtlen // 4 + 1, interval, index):
        if EUDIf()(t == txtlen // 4):
            ret << 1
        if EUDElse()():
            ret << 0
            if EUDIf()(t >= 1):
                f_bwrite_epd(ct.epd + t - 1, 3, 0x05)
            EUDEndIf()
            if EUDIf()(t <= txtlen // 4 - 1):
                f_bwrite_epd(ct.epd + t, 3, 0x14)
            EUDEndIf()
        EUDEndIf()
    DoActions(DisplayText(ct.strBuffer))
    return ret


@EUDFunc
def f_sum(var, Max):
    if EUDIf()(var >= Max):
        EUDReturn(var - Max)
    if EUDElse()():
        EUDReturn(var)
    EUDEndIf()


def f_rainbow(*args, interval=1):
    ret = EUDVariable()
    txtList, txtlen = f_procString(*args)
    # ct.f_reset_epd()
    ct.f_makeText_epd(*txtList)
    ct.f_reset()
    colors = [0x08, 0x11, 0x17, 0x07, 0x1F, 0x1C, 0x10]
    for t in tL.Timeline(txtlen // 4, interval):
        for i, c in enumerate(colors):
            f_bwrite_epd(ct.epd + f_sum(t + 2 * i, txtlen // 4), 3, c)
            f_bwrite_epd(ct.epd + f_sum(t + 1 + 2 * i, txtlen // 4), 3, c)
    DoActions(DisplayText(ct.strBuffer))
    return ret


def f_fadeOut(*args, interval=1, index=0):
    txtList, txtlen = f_procString(*args)
    # ct.f_reset_epd()
    ct.f_makeText_epd(*txtList)
    ct.f_reset()
    for t in tL.Timeless(txtlen // 4 + 3, interval, index):
        s = txtlen // 4 + 2 - t
        if EUDIf()(t >= 3):
            f_bwrite_epd(ct.epd + s, 3, 0x14)
        EUDEndIf()
        if EUDIf()([t >= 2, t <= txtlen // 4 + 1]):
            f_bwrite_epd(ct.epd + s - 1, 3, 0x05)
        EUDEndIf()
        if EUDIf()([t >= 1, t <= txtlen // 4]):
            f_bwrite_epd(ct.epd + s - 2, 3, 0x04)
        EUDEndIf()
        if EUDIf()(t <= txtlen // 4 - 1):
            f_bwrite_epd(ct.epd + s - 3, 3, 0x03)
        EUDEndIf()
    DoActions(DisplayText(ct.strBuffer))

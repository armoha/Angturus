from eudplib import *
import customText3 as ct

'''
버튼셋
스킬1~8: 41, 42, 37, 38, 39, 43, 45, 46  # 즉발
스킬9~16: 66, 67, 71, 72, 83, 84, 44, 50
스킬1~8:  # 타겟팅
팧　 4 / 6
엘리 14 / 18
에알 24 / 26
페어 31 / 33
더페 85 / 101

### 타겟팅
락다 EMP 브루 115/122/121
이레디 야마토 닥쉄 143/113/119
플그 인스 144/146

스톰 패러 컨슘 142/120/145
스테시스 리스토 웹 147/180/181
옵티컬 마엘 185/186
'''
Instant = EUDArray([41, 42, 37, 38, 39, 43, 45, 46, 66, 67, 71, 72, 83, 84, 44, 50])
Target = EUDArray([1, 2, 13, 7, 8, 14, 15, 17, 19, 18, 16, 22, 24, 25, 30, 31])
Tooltip = [[1343 + 16 * x + a for a in range(16)] for x in range(5)]
btnUnit = EUDArray([4, 6, 14, 18, 24, 26, 31, 33, 85, 101])


@EUDFunc
def f_getSkillInfo(char, no):
    pass


@EUDFunc
def f_SetSkillTooltip(char, no, skill):
    dst = ct.f_getTblPtr(1343 + 16 * char + no) + 7
    EUDSwitch(skill)
    ct.f_dbstr_print(dst, *args)
    EUDEndSwitch()


@EUDFunc
def f_SetSkillButton(char, no, icon, flag):
    EncodeSwitch
    Index = 2 * char + no // 8
    btnEPD = f_epdread_epd(EPD(0x5187EC) + 3 * btnUnit[Index]) + 5 * (no % 8)
    DoActions(SetMemoryEPD(btnEPD, SetTo, icon * 65536 + no + 1))
    if EUDIf()(flag == 0):
        DoActions([  # Instant
            SetMemoryEPD(btnEPD + 2, SetTo, 4338864),
            SetMemoryEPD(btnEPD + 3, SetTo, Instant[no] * 65536)
        ])
    if EUDElseIf()(flag == 1):
        DoActions([  # Targeting
            SetMemoryEPD(btnEPD + 2, SetTo, 4341616),
            SetMemoryEPD(btnEPD + 3, SetTo, Target[no] * 65536)
        ])
    EUDEndIf()


@EUDFunc
def f_SkillButtonReload(char):
    for n in EUDLoopRange(16):
        icon, flag, skill = f_getSkillInfo(n)
        f_SetSkillTooltip(char, n, skill)
        f_SetSkillButton(char, n, icon, flag)

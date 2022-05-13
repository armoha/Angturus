from eudplib import *


@EUDFunc
def _EPD2Ptr(epd):
    pass


def EPD2Ptr(epd):
    epdcache = epd.Exactly(EPD(0))
    RawTrigger()


def EUDAssert(condition, error_message=None):
    condition.Negate()
    if error_message is None:
        import inspect

        frame = inspect.getouterframes(inspect.currentframe())[1]
        filename = frame.filename.removeprefix("E:\\StarCraft\\").removeprefix("Maps\\")
        error_message = f"\x04fn {frame.function} in {filename}:{frame.lineno}"
    Trigger(
        condition,
        [
            [
                [SetMemory(0x6509B0, SetTo, p), DisplayText(error_message)]
                for p in range(5)
            ],
            SetMemory(0xFFFFFFFF - 0x1DEADB0B, SetTo, 0),
        ],
    )


@cachedfunc
def Container(size, basetype=None):
    assert isinstance(size, int) and size > 0

    class _Container(EUDStruct):
        _fields_ = ["data", "view", "pos"]

        def constructor(self, initvals=None):
            if initvals is None:
                initvals = [0] * size
            viewval = EPD(self.view.getValueAddr())
            # (player, modifier, value, bitmask)
            self.data = EPD(
                EUDVArray(size)(initvals, dest=viewval, nextptr=self.view.GetVTable())
            )
            self.pos = self.data + 87

        @EUDMethod
        def __iadd__(self, value):
            EUDAssert(self.pos < self.data + 87 + 18 * size)
            f_dwwrite_epd(self.pos, value)
            self.pos += 18

        def __iter__(self):
            dataptr = EPD2Ptr(self.data)

            if EUDWhile()(True):
                yield self.view
            EUDEndWhile()

    return _Container

def crash():
    _sampleStackFrame0(1337)

def _sampleStackFrame0(n):
    m = n + 9001
    _sampleStackFrame1(m)

def _sampleStackFrame1(n):
    _sampleStackFrame2(n)

def _sampleStackFrame2(n):
    x = 1 / 0
from functools import wraps
import maya.cmds as mc

def mayaUndoRun(func):
    """ Puts the wrapped `func` into a single Maya Undo action, then undoes it when the function enters the finally: block
    将包装好的' func '放入单个Maya Undo动作中，然后在函数进入finally:块时撤消它"""
    @wraps(func)
    def _undofunc(*args, **kwargs):
        try:
            # start an undo chunk
            # 开始撤销块
            mc.undoInfo(openChunk=True)
            return func(*args, **kwargs)
        finally:
            # after calling the func, end the undo chunk
            # 调用该函数后，结束撤消块
            mc.undoInfo(closeChunk=True)

    return _undofunc
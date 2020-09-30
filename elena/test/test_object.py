import unittest


class QualityController:
    def __init__(self):
        self.inspection_workpiece = None

    def confirm(self):
        print("I am QC")


class Workcell():
    def __init__(self):
        self.workpiece = None
        
    def start(self, workpiece):
        self.workpiece = workpiece
        self.workpiece.progress = "in progress"
        # return self.workpiece

    def end(self):
        self.workpiece.progress = "done"
        self.workpiece = None


class Workpiece:
    def __init__(self):
        self.progress = "not started"


class TesterObject(unittest.TestCase):
    def test_obj_in_obj(self):
        wc1 = Workcell()
        wp1 = Workpiece()
        print(f"instantiated {wc1.workpiece}")
        print(f"instantiated {wp1.progress}")
        wc1.start(wp1)
        print(f"started {wc1.workpiece}")
        print(f"started {wp1.progress}")
        wc1.end()
        print(f"ended {wc1.workpiece}")
        print(f"ended {wp1.progress}")

    def test_change_superclass(self):
        wc1 = Workcell()
        print(wc1.__class__)
        print(wc1.__class__.__base__)
        # cls = object.__class__
        # object.__class__ = cls.__class__(cls.__name__ + "WithExtraBase", (cls, ExtraBase), {})
        wc1.__class__.__base__ += (QualityController,)
        print(wc1.__class__.__base__)
        # print(isinstance(wc1, QualityController))
        # wc1.confirm()

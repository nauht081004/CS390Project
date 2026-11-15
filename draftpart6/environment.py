"""Lexically nested runtime environments for ANVI."""
class EnvironmentError(Exception): pass
class Environment:
    def __init__(self, parent=None): self.values={}; self.parent=parent
    def define(self,name,value): self.values[name]=value
    def get(self,name):
        if name in self.values: return self.values[name]
        if self.parent is not None: return self.parent.get(name)
        raise EnvironmentError(f"undefined variable '{name}'")
    def assign(self,name,value):
        if name in self.values: self.values[name]=value; return
        if self.parent is not None and self.parent.contains(name): self.parent.assign(name,value); return
        raise EnvironmentError(f"cannot assign to undefined variable '{name}'")
    def contains(self,name): return name in self.values or (self.parent is not None and self.parent.contains(name))
    def snapshot(self): return dict(self.values)

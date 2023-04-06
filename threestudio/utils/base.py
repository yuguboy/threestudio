from dataclasses import dataclass
from threestudio.utils.typing import *
import torch
import torch.nn as nn

from threestudio.utils.config import parse_structured
from threestudio.utils.misc import get_device


class Configurable:
    @dataclass
    class Config:
        pass

    def __init__(self, cfg: Optional[dict] = None) -> None:
        super().__init__()
        self.cfg = parse_structured(self.Config, cfg)


class Updateable:
    def do_update_step(self, epoch: int, global_step: int):
        for attr in self.__dir__():
            try:
                attr = getattr(self, attr)
            except:
                continue # ignore attributes like property, which can't be retrived using getattr?
            if isinstance(attr, Updateable):
                attr.do_update_step(epoch, global_step)
        self.update_step(epoch, global_step)

    def update_step(self, epoch: int, global_step: int):
        pass


class BaseModule(nn.Module, Updateable):
    @dataclass
    class Config:
        configure_at_runtime: bool = False

    cfg: Config # add this to every subclass of BaseModule to enable static type checking

    def __init__(self, cfg: Optional[Union[dict, DictConfig]] = None, *args, **kwargs) -> None:
        super().__init__()
        self.cfg = parse_structured(self.Config, cfg)
        self.device = get_device()
        self.ready = False
        if not self.cfg.configure_at_runtime:
            self.configure(*args, **kwargs)
            self.ready = True
    
    def configure(self, *args, **kwargs) -> None:
        pass
        
from __future__ import annotations
from enum import Enum
from utils import dictdiff

NUM_PHASES=5

class TornadoscopeVariables(Enum):
    state = 1
    freq = 2
    ampliX = 3
    ampliY = 4
    phaseY = 5
    multY = 6
    expo = 7
    phase = 8
    phase_state = 9
    phase_hue_auto = 10
    phase_trig_auto = 11
    phase_hue_val = 12
    phase_trig_val = 13
    phase_hue_step = 14
    phase_trig_step = 15

tv = TornadoscopeVariables

class TornadoscopeState:
    def __init__(self, global_state, phases) -> None:
        self.global_state = global_state
        self.phases = phases

    @classmethod
    def from_defaults(cls):
        global_state = {
            tv.state: 1,
            tv.freq: 15,
            tv.ampliX: 50,
            tv.ampliY: 50,
            tv.phaseY: 255 // 4,
            tv.multY: 1,
            tv.expo: 831,
        }
        phases = [{
                tv.phase: i,
                tv.phase_state: 0,
                tv.phase_hue_auto: 0,
                tv.phase_trig_auto: 0,
                tv.phase_hue_val: 0,
                tv.phase_trig_val: 0,
                tv.phase_hue_step: 0,
                tv.phase_trig_step: 0,
            } for i in range(NUM_PHASES)
        ]
        return cls(global_state, phases)
    
    @classmethod
    def from_overrides(cls, global_state={}, phases=[]):
        d = cls.from_defaults()
        d.global_state |= global_state
        new_phases = phases + [{}] * (len(d.phases) - len(phases))
        for dp, newp in zip(d.phases, new_phases):
            dp |= newp
        return d

    def diff(self, other: TornadoscopeState):
        gs_diff = dictdiff(self.global_state, other.global_state)
        phases_diff = [dictdiff(p, newp) for p, newp in zip(self.phases, other.phases)]
        return gs_diff, phases_diff
    
    def apply_diff(self, diff):
        gs, phases = diff
        self.global_state |= gs
        for p, newp in zip(self.phases, phases):
            p |= newp
    
if __name__ == "__main__":
    ts = TornadoscopeState.from_overrides({tv.freq: 111}, [{tv.phase_state: 1, tv.phase_hue_val: 100}])
    print(ts)
    ts2 = TornadoscopeState.from_overrides({tv.ampliX: 22}, [{}, {tv.phase_state: 1, tv.phase_hue_val: 200}])
    diff = ts.diff(ts2)
    print(f"{diff}")
    ts.apply_diff(diff)
    print(ts)
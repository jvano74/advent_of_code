from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 20: Pulse Propagation ---
    With your help, the Elves manage to find the right parts and fix all of the
    machines. Now, they just need to send the command to boot up the machines
    and get the sand flowing again.

    The machines are far apart and wired together with long cables. The cables
    don't connect to the machines directly, but rather to communication modules
    attached to the machines that perform various initialization tasks and also
    act as communication relays.

    Modules communicate using pulses. Each pulse is either a high pulse or a low
    pulse. When a module sends a pulse, it sends that type of pulse to each
    module in its list of destination modules.

    There are several different types of modules:

    - Flip-flop modules (prefix %) are either on or off; they are initially off.
      If a flip-flop module receives a high pulse, it is ignored and nothing
      happens. However, if a flip-flop module receives a low pulse, it flips
      between on and off. If it was off, it turns on and sends a high pulse. If
      it was on, it turns off and sends a low pulse.

    - Conjunction modules (prefix &) remember the type of the most recent pulse
      received from each of their connected input modules; they initially
      default to remembering a low pulse for each input. When a pulse is
      received, the conjunction module first updates its memory for that input.
      Then, if it remembers high pulses for all inputs, it sends a low pulse;
      otherwise, it sends a high pulse.

    - There is a single broadcast module (named broadcaster). When it receives a
      pulse, it sends the same pulse to all of its destination modules.

    - Here at Desert Machine Headquarters, there is a module with a single
      button on it called, aptly, the button module. When you push the button, a
      single low pulse is sent directly to the broadcaster module.

    After pushing the button, you must wait until all pulses have been delivered
    and fully handled before pushing it again. Never push the button if modules
    are still processing pulses.

    Pulses are always processed in the order they are sent. So, if a pulse is
    sent to modules a, b, and c, and then module a processes its pulse and sends
    more pulses, the pulses sent to modules b and c would have to be handled
    first.

    The module configuration (your puzzle input) lists each module. The name of
    the module is preceded by a symbol identifying its type, if any. The name is
    then followed by an arrow and a list of its destination modules. For
    example:

    broadcaster -> a, b, c
    %a -> b
    %b -> c
    %c -> inv
    &inv -> a

    In this module configuration, the broadcaster has three destination modules
    named a, b, and c. Each of these modules is a flip-flop module (as indicated
    by the % prefix). a outputs to b which outputs to c which outputs to another
    module named inv. inv is a conjunction module (as indicated by the & prefix)
    which, because it has only one input, acts like an inverter (it sends the
    opposite of the pulse type it receives); it outputs to a.

    By pushing the button once, the following pulses are sent:

    button -low-> broadcaster
    broadcaster -low-> a
    broadcaster -low-> b
    broadcaster -low-> c
    a -high-> b
    b -high-> c
    c -high-> inv
    inv -low-> a
    a -low-> b
    b -low-> c
    c -low-> inv
    inv -high-> a

    After this sequence, the flip-flop modules all end up off, so pushing the
    button again repeats the same sequence.

    Here's a more interesting example:

    broadcaster -> a
    %a -> inv, con
    &inv -> b
    %b -> con
    &con -> output

    This module configuration includes the broadcaster, two flip-flops (named a
    and b), a single-input conjunction module (inv), a multi-input conjunction
    module (con), and an untyped module named output (for testing purposes). The
    multi-input conjunction module con watches the two flip-flop modules and, if
    they're both on, sends a low pulse to the output module.

    Here's what happens if you push the button once:

    button -low-> broadcaster
    broadcaster -low-> a
    a -high-> inv
    a -high-> con
    inv -low-> b
    con -high-> output
    b -high-> con
    con -low-> output

    Both flip-flops turn on and a low pulse is sent to output! However, now that
    both flip-flops are on and con remembers a high pulse from each of its two
    inputs, pushing the button a second time does something different:

    button -low-> broadcaster
    broadcaster -low-> a
    a -low-> inv
    a -low-> con
    inv -high-> b
    con -high-> output

    Flip-flop a turns off! Now, con remembers a low pulse from module a, and so
    it sends only a high pulse to output.

    Push the button a third time:

    button -low-> broadcaster
    broadcaster -low-> a
    a -high-> inv
    a -high-> con
    inv -low-> b
    con -low-> output
    b -low-> con
    con -high-> output

    This time, flip-flop a turns on, then flip-flop b turns off. However, before
    b can turn off, the pulse sent to con is handled first, so it briefly
    remembers all high pulses for its inputs and sends a low pulse to output.
    After that, flip-flop b turns off, which causes con to update its state and
    send a high pulse to output.

    Finally, with a on and b off, push the button a fourth time:

    button -low-> broadcaster
    broadcaster -low-> a
    a -low-> inv
    a -low-> con
    inv -high-> b
    con -high-> output

    This completes the cycle: a turns off, causing con to remember only low
    pulses and restoring all modules to their original states.

    To get the cables warmed up, the Elves have pushed the button 1000 times.
    How many pulses got sent as a result (including the pulses sent by the
    button itself)?

    In the first example, the same thing happens every time the button is
    pushed: 8 low pulses and 4 high pulses are sent. So, after pushing the
    button 1000 times, 8000 low pulses and 4000 high pulses are sent.
    Multiplying these together gives 32000000.

    In the second example, after pushing the button 1000 times, 4250 low pulses
    and 2750 high pulses are sent. Multiplying these together gives 11687500.

    Consult your module configuration; determine the number of low pulses and
    high pulses that would be sent after pushing the button 1000 times, waiting
    for all pulses to be fully handled after each push of the button. What do
    you get if you multiply the total number of low pulses sent by the total
    number of high pulses sent?

    Your puzzle answer was 898557000.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The final machine responsible for moving the sand down to Island Island has
    a module attached named rx. The machine turns on when a single low pulse is
    sent to rx.

    Reset all modules to their default states. Waiting for all pulses to be
    fully handled after each button press, what is the fewest number of button
    presses required to deliver a single low pulse to the module named rx?

    Your puzzle answer was 238420328103151.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


SAMPLE_1 = [
    "broadcaster -> a, b, c",
    "%a -> b",
    "%b -> c",
    "%c -> inv",
    "&inv -> a",
]

SAMPLE_2 = [
    "broadcaster -> a",
    "%a -> inv, con",
    "&inv -> b",
    "%b -> con",
    "&con -> output",
]

with open(Path(__file__).parent / "2023_20_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")


class Machine:
    def __init__(self, raw_components) -> None:
        self.fwd_link = defaultdict(list)
        self.back_link = defaultdict(dict)
        self.state = defaultdict(int)
        self.operation = defaultdict(str)
        self.totals = defaultdict(int)
        self.node_hx = defaultdict(dict)
        self.push_count = 0
        for component in raw_components:
            label, raw_destinations = component.split(" -> ")
            if label != "broadcaster":
                op = label[0]
                label = label[1:]
            else:
                op = "broadcast"
            self.operation[label] = op
            self.fwd_link[label] = raw_destinations.split(", ")
            for target in self.fwd_link[label]:
                self.back_link[target][label] = 0

    def push(self, display=False):
        self.push_count += 1
        source = "button"
        pulse = 0
        target = "broadcaster"
        next_actions = [(target, pulse, source)]
        self.totals[pulse] += 1
        sub_count = 0

        while next_actions:
            sub_count += 1
            target, pulse, source = next_actions.pop(0)
            op = self.operation[target]
            self.node_hx[target][(self.push_count, sub_count)] = pulse
            if display:
                print(f"{source} --[{pulse}]--> {target} {op=}")
            if op == "broadcast":
                output_state = pulse
            elif op == "%":  # Flip-flop
                if pulse != 0:
                    continue
                self.state[target] = 1 - self.state[target]
                output_state = self.state[target]
            elif op == "&":  # Conjunction
                self.back_link[target][source] = pulse
                if 0 in self.back_link[target].values():
                    output_state = 1
                else:
                    output_state = 0
            for new_target in self.fwd_link[target]:
                next_actions.append((new_target, output_state, target))
                self.totals[output_state] += 1


def test_machine():
    # part 1
    sample_machine_1 = Machine(SAMPLE_1)
    # sample_machine_1.push(display=True)
    for _ in range(1000):
        sample_machine_1.push()
    totals = sample_machine_1.totals
    prod = totals[0] * totals[1]
    assert prod == 32000000

    sample_machine_2 = Machine(SAMPLE_2)
    # print("===== Push 1 =====")
    # sample_machine_2.push(display=True)
    # print("===== Push 2 =====")
    # sample_machine_2.push(display=True)
    # print("===== Push 3 =====")
    # sample_machine_2.push(display=True)
    # print("===== Push 4 =====")
    # sample_machine_2.push(display=True)
    for _ in range(1000):
        sample_machine_2.push()
    totals = sample_machine_2.totals
    prod = totals[0] * totals[1]
    # print(totals)
    assert prod == 11687500

    my_machine = Machine(RAW_INPUT)
    for _ in range(1000):
        my_machine.push()
    totals = my_machine.totals
    prod = totals[0] * totals[1]
    assert prod == 898557000

    # part 2
    # rx_back = my_machine.back_link["rx"]  # "qb"
    # assert [k for k in rx_back.keys()] == ["qb"]
    # all_high = my_machine.back_link["qb"]
    # for node in all_high.keys():
    #     hx = my_machine.node_hx[node]
    #     print(f"{node=} {hx=}")
    #
    # Ended up simply working by hand isolating the 4 counter circuits built from the flip flop
    assert 4003 * 3911 * 3739 * 4073 == 238420328103151

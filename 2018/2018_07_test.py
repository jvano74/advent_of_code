from pathlib import Path
from collections import defaultdict


SAMPLE = [
    "Step C must be finished before step A can begin.",
    "Step C must be finished before step F can begin.",
    "Step A must be finished before step B can begin.",
    "Step A must be finished before step D can begin.",
    "Step B must be finished before step E can begin.",
    "Step D must be finished before step E can begin.",
    "Step F must be finished before step E can begin",
]

with open(Path(__file__).parent / "2018_07_input.txt") as fp:
    INPUT = [line.strip() for line in fp]


class Part1:
    """
    --- Day 7: The Sum of Its Parts ---
    You find yourself standing on a snow-covered coastline; apparently, you landed a little off course.
    The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be
    trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating
    a paradox by asking them for directions.

    "Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018
    speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator?
    "Those clothes don't look very warm; take this." They hand you a heavy coat.

    "We do need to find our way back to the North Pole, but we have higher priorities at the moment. You
    see, believe it or not, this box contains something that will solve all of Santa's transportation
    problems - at least, that's what it looks like from the pictures in the instructions." It doesn't
    seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

    "'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start
    excitedly pulling more parts out of the box.

    The instructions specify a series of steps and requirements about which steps must be finished
    before others can begin (your puzzle input). Each step is designated by a single letter.

    For example, suppose you have the following instructions:

    - Step C must be finished before step A can begin.
    - Step C must be finished before step F can begin.
    - Step A must be finished before step B can begin.
    - Step A must be finished before step D can begin.
    - Step B must be finished before step E can begin.
    - Step D must be finished before step E can begin.
    - Step F must be finished before step E can begin.

    Visually, these requirements look like this:

      -->A--->B--
     /   \\      \\
    C      -->D----->E
     \\           /
      ---->F-----

    Your first goal is to determine the order in which the steps should be completed.
    If more than one step is ready, choose the step which is first alphabetically.
    In this example, the steps would be completed as follows:

    - Only C is available, and so it is done first.
    - Next, both A and F are available. A is first alphabetically, so it is done next.
    - Then, even though F was available earlier, steps B and D are now also available,
      and B is the first alphabetically of the three.
    - After that, only D and F are available. E is not available because only some of
      its prerequisites are complete. Therefore, D is completed next.
    - F is the only choice, so it is done next.
    - Finally, E is completed.

    So, in this example, the correct order is CABDFE.

    In what order should the steps in your instructions be completed?
    """

    pass


def find_order(instructions):
    possible_next_graph = defaultdict(list)
    pre_req_graph = defaultdict(list)
    starts = set()
    ends = set()
    for line in instructions:
        words = line.split(" ")
        start = words[1]
        end = words[-3]
        starts.add(start)
        ends.add(end)
        possible_next_graph[start].append(end)
        pre_req_graph[end].append(start)
    step_options = starts - ends
    built = []
    while len(step_options) > 0:
        next_step = ""
        options = sorted(step_options)
        while next_step == "":
            possible_next_step = options.pop(0)
            if all((needed in built) for needed in pre_req_graph[possible_next_step]):
                next_step = possible_next_step
        built.append(next_step)
        step_options.discard(next_step)
        for now_possible in possible_next_graph[next_step]:
            if now_possible not in built:
                step_options.add(now_possible)
    return "".join(built)


def test_find_order():
    assert find_order(SAMPLE) == "CABDFE"
    assert find_order(INPUT) == "BGJCNLQUYIFMOEZTADKSPVXRHW"


class Part2:
    """
    --- Part Two ---
    As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll
    go faster if we work together." Now, you need to account for multiple people working on steps simultaneously.
    If multiple steps are available, workers should still begin them in alphabetical order.

    Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A
    takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

    To simplify things for the example, however, suppose you only have help from one Elf (a total of two
    workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26
    seconds). Then, using the same instructions as above, this is how each second would be spent:

    Second   Worker 1   Worker 2   Done
       0        C          .
       1        C          .
       2        C          .
       3        A          F       C
       4        B          F       CA
       5        B          F       CA
       6        D          F       CAB
       7        D          F       CAB
       8        D          F       CAB
       9        D          .       CABF
      10        E          .       CABFD
      11        E          .       CABFD
      12        E          .       CABFD
      13        E          .       CABFD
      14        E          .       CABFD
      15        .          .       CABFDE

    Each row represents one second of time. The Second column identifies how many seconds have passed
    as of the beginning of that second. Each worker column shows the step that worker is currently doing
    (or . if they are idle). The Done column shows completed steps.

    Note that the order of the steps has changed; this is because steps now take time to finish and
    multiple workers can begin multiple steps simultaneously.

    In this example, it would take 15 seconds for two workers to complete these steps.

    With 5 workers and the 60+ second step durations described above, how long will it take to complete
    all of the steps?
    """

    pass


class WorkShop:
    def __init__(self, instructions, number_of_workers=1, base_time=0):
        self.possible_next_graph = defaultdict(list)
        self.pre_req_graph = defaultdict(list)
        starts = set()
        ends = set()
        for line in instructions:
            words = line.split(" ")
            start = words[1]
            end = words[-3]
            starts.add(start)
            ends.add(end)
            self.possible_next_graph[start].append(end)
            self.pre_req_graph[end].append(start)
        self.next_work = starts - ends

        self.work_time = 0
        self.base_time = base_time
        self.workers_waiting = set(range(number_of_workers))
        self.workers_working = defaultdict(list)
        self.next_work = starts - ends
        self.blocked_work = set()
        self.work_completed = []

    def find_time(self):
        while len(self.next_work) > 0 or len(self.workers_working) > 0:
            if len(self.workers_waiting) == 0:
                self.advance_time()
            elif len(self.next_work) == 0:
                self.advance_time()
            else:
                self.assign_worker()
                print(self.work_time, self.workers_working, self.work_completed)
        return "".join(self.work_completed), self.work_time

    def advance_time(self):
        print(f"== >{self.workers_working}")
        self.work_time = min(self.workers_working)
        self.work_completed.append(f"{self.work_time}:")
        for worker, work_job in self.workers_working[self.work_time]:
            self.workers_waiting.add(worker)
            self.work_completed.append(
                work_job
            )  # if multiple workers finish at same time could sort
            for now_maybe_possible in self.possible_next_graph[work_job]:
                if now_maybe_possible not in self.work_completed:
                    self.blocked_work.add(now_maybe_possible)
        for now_maybe_possible in self.blocked_work:
            if all(
                (required in self.work_completed)
                for required in self.pre_req_graph[now_maybe_possible]
            ):
                self.next_work.add(now_maybe_possible)
        self.blocked_work = self.blocked_work - self.next_work

        del self.workers_working[self.work_time]

    def assign_worker(self):
        while len(self.workers_waiting) > 0 and len(self.next_work) > 0:
            worker = self.workers_waiting.pop()
            next_step = min(self.next_work)
            finish_time = self.work_time + self.base_time + ord(next_step) - 64
            self.workers_working[finish_time].append((worker, next_step))
            self.next_work.discard(next_step)


def test_find_time():
    sample_workshop = WorkShop(SAMPLE, 2)
    assert sample_workshop.find_time() == ("3:C4:A6:B9:F10:D15:E", 15)
    print("Something is wrong?")
    workshop = WorkShop(INPUT, 5, 60)
    assert workshop.find_time() == (
        "62:B"
        + "129:G"
        + "199:J"
        + "206:Q"
        + "210:U"
        + "214:Y"
        + "262:C"
        + "273:N"
        + "289:O"
        + "342:I"
        + "345:L"
        + "375:Z"
        + "408:F"
        + "415:M"
        + "480:E"
        + "488:T"
        + "549:A"
        + "559:K"
        + "613:D"
        + "628:S"
        + "704:P"
        + "786:V"
        + "788:X"
        + "866:R"
        + "934:H"
        + "1017:W",
        1017,
    )
    # 1911 was too high

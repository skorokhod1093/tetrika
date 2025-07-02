from abc import ABC, abstractmethod

class AppearanceError(Exception):
    """Исключение для ошибок вычисления времени присутствия."""
    pass

class IntervalMerger(ABC):
    @abstractmethod
    def merge(self, intervals: list[int]) -> list[tuple[int, int]]:
        pass

class SimpleIntervalMerger(IntervalMerger):
    def merge(self, intervals: list[int]) -> list[tuple[int, int]]:
        if not intervals:
            return []
        pairs = sorted([(intervals[i], intervals[i+1]) for i in range(0, len(intervals), 2)])
        merged = []
        for start, end in pairs:
            if not merged or merged[-1][1] < start:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
        return [(s, e) for s, e in merged]

class IntervalIntersection:
    @staticmethod
    def intersect(a: list[tuple[int, int]], b: list[tuple[int, int]]) -> list[tuple[int, int]]:
        result = []
        i = j = 0
        while i < len(a) and j < len(b):
            start = max(a[i][0], b[j][0])
            end = min(a[i][1], b[j][1])
            if start < end:
                result.append((start, end))
            if a[i][1] < b[j][1]:
                i += 1
            else:
                j += 1
        return result

class AppearanceCalculator:
    def __init__(self, merger: IntervalMerger = None):
        self.merger = merger or SimpleIntervalMerger()

    def appearance(self, intervals: dict[str, list[int]]) -> int:
        try:
            lesson = self.merger.merge(intervals['lesson'])
            pupil = self.merger.merge(intervals['pupil'])
            tutor = self.merger.merge(intervals['tutor'])
            if not lesson or not pupil or not tutor:
                raise AppearanceError("Один или несколько интервалов пусты")
            pupil_in = IntervalIntersection.intersect(pupil, lesson)
            tutor_in = IntervalIntersection.intersect(tutor, lesson)
            both = IntervalIntersection.intersect(pupil_in, tutor_in)
            return sum(end - start for start, end in both)
        except Exception as e:
            raise AppearanceError(f"Ошибка вычисления времени: {e}") 
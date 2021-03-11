from Domain.Indicators.Indicator import Indicator


class MockIndicator(Indicator):

    def __init__(self, pattern, time_scale, budget, partition_size, n_partition_limit):
        super().__init__(pattern, time_scale, budget, partition_size, n_partition_limit)

    def ingest(self, array):
        pass

    def get_max_arr_len(self):
        return 10

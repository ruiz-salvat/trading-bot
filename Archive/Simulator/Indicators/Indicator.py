from abc import ABC, abstractmethod


class Indicator(ABC):

    def __init__(self, pattern, symbol, time_scale, budget, partition_size, n_partition_limit):
        self.pattern = pattern
        self.symbol = symbol
        self.time_scale = time_scale
        self.initial_budget = budget
        self.budget = budget
        self.partition_size = partition_size
        self.coins = 0
        self.n_partitions = 0
        self.n_total_partitions = 0
        self.clean_gains = 0
        self.n_partition_limit = n_partition_limit
        self.ingested = False
        self.result = None

    def reduce(self, array):
        new_array = []
        counter = 0
        aux_value = 0
        if self.time_scale > 1:
            for value in array:
                if counter >= self.time_scale - 1:
                    aux_value = aux_value + value  # inserts the remaining value
                    aux_value = aux_value / self.time_scale
                    new_array.append(aux_value)
                    aux_value = 0
                    counter = 0
                else:
                    aux_value = aux_value + value
                    counter += 1
            if counter > 0:
                aux_value = aux_value / (counter + 1)
                new_array.append(aux_value)
            return new_array
        else:
            return array

    @abstractmethod
    def ingest(self, array):
        pass

    def buy(self, price):
        if self.budget >= self.partition_size:
            self.coins = self.coins + self.partition_size / price
            self.budget = self.budget - self.partition_size
            self.n_partitions += 1
            self.n_total_partitions += 1

    def sell(self, price):
        if self.n_partitions > 0:
            sold_coins = self.coins / self.n_partitions
            self.coins = self.coins - sold_coins
            self.budget = self.budget + sold_coins * price
            self.clean_gains = self.clean_gains + (sold_coins * price - self.partition_size)
            self.n_partitions -= 1

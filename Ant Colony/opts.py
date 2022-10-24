class AntColonyAlgParams:
    def __init__(self, alfa, beta, ant_amount, consistency_percentage, evaporation_coeff) -> None:
        if not self.__check_in_range(consistency_percentage) or not self.__check_in_range(evaporation_coeff):
            raise Exception(
                'Consistency_percentage and evaporation_coeff should be in range from 0.0 to 1.0!')

        self.alfa = alfa
        self.beta = beta
        self.ant_amount = ant_amount
        self.consistency_percentage = consistency_percentage
        self.after_evaporation = 1.0 - evaporation_coeff

    def __check_in_range(self, val, lower_bound=0.0, heigher_bound=1.0):
        return val > lower_bound and val < heigher_bound

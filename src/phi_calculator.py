def Method3(t1, t2, t3, t4):
    return float(t1 - t2 + t4 - t3) / 2


class PhiCalculator:
    """PhiCalculator"""
    def __init__(self, method=Method3):
        self.method = method
    
    def calculate(self, t1, t2, t3, t4):
        return self.method(t1, t2, t3, t4)

    def pair_and_verify(self, t1_pps, t2_pps):
        t1_reference_in_seconds = []
        actual_phi = []

        l = len(t1_pps)
        for i in range(0, l):
            # ignore the cycle if any is zero
            if t1_pps[i] == '0' or t2_pps[i] == '0':
                continue

            # reference time in seconds
            time_seconds = int(int(t1_pps[i]) / 1e6)
            t1_reference_in_seconds.append(float(time_seconds))

            # actual phi in microseconds
            actual_phi_value = float(t1_pps[i]) - float(t2_pps[i])

            # correct phase shifts
            if actual_phi_value < 0:
                actual_phi.append(actual_phi_value + 1e6)
            else:
                actual_phi.append(actual_phi_value)
        
        return t1_reference_in_seconds, actual_phi

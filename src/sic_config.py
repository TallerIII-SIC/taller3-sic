import ConfigParser
import os
import numpy as np

class Configuration:
    """SIC algorithm configuration."""
    def __init__(self, config_file_name, base_dir=os.getcwd()):
        self.base_dir = base_dir

        config = ConfigParser.ConfigParser()
        config.read(self._concat_base(config_file_name))

        self.t1_pps_file = self._concat_base(config.get("calcula_error_cfg", "t1_pps"))
        self.t2_pps_file = self._concat_base(config.get("calcula_error_cfg", "t2_pps"))
        self.client_log_file = self._concat_base(config.get("calcula_error_cfg", "log"))

    def _concat_base(self, file_name):
        """Concatenates the base_dir with a file name, in an OS independent way."""
        return os.path.join(self.base_dir, file_name)

    def get_t1_pps_file_name(self):
        return self.t1_pps_file

    def get_t2_pps_file_name(self):
        return self.t2_pps_file

    def get_client_log_file_name(self):
        return self.client_log_file


class FileReader:
    """File reader with SIC format."""
    def __init__(self, config, phi_calculator):
        self.config = config
        self.phi_calculator = phi_calculator
        self.phi_array = None
        self.t1_array = None
        self.rtt_array = None

    def _read_times(self):
        """Internal method to read phi and t1 values from the client log file."""
        log_file = self.config.get_client_log_file_name()
        lines = np.loadtxt(log_file, dtype=int, delimiter='|')

        self.phi_array = np.zeros(len(lines))
        self.t1_array = np.zeros(len(lines))
        self.rtt_array = np.zeros(len(lines))

        for line_number, line in enumerate(lines):
            t1, t2, t3, t4 = line

            phi = self.phi_calculator.calculate(t1, t2, t3, t4)
            self.phi_array[line_number] = phi

            # reference time in seconds
            self.t1_array[line_number] = int(t1 / 1e6)
            self.rtt_array[line_number] = float(t4 - t1)

    def get_phi_values(self):
        """Returns the phi values."""
        if self.phi_array is None:
            self._read_times()

        return self.phi_array

    def get_t1_values(self):
        """Returns the t1 values."""
        if self.t1_array is None:
            self._read_times()

        return self.t1_array

    def get_rtt_values(self):
        """Returns the t1 values."""
        if self.rtt_array is None:
            self._read_times()

        return self.rtt_array

    def _read_pps_file(self, pps_file_name):
        output = []

        with open(pps_file_name, 'r') as pps_file:
            pps_lines = pps_file.readlines()

        first_value_seconds = int(pps_lines[0][:-7])
        last_value_seconds = int(pps_lines[-1][:-7])

        index = 0
        for second in range(first_value_seconds, last_value_seconds + 1):
            cur_time_seconds = int(pps_lines[index][:-7])
            cur_time_microseconds = pps_lines[index].split('\n')[0]

            if second == cur_time_seconds:                 
                output.append(cur_time_microseconds) ## if match at seconds, add the value to output
                index += 1                           ## move the current time
            else:
                output.append('0')                   ## otherwise, add a zero
                if(pps_lines[index][:-7].split('\n')[0] == '0'): 
                    index += 1

        return output

    def get_t1_pps_values(self):
        return self._read_pps_file(self.config.get_t1_pps_file_name())

    def get_t2_pps_values(self):
        return self._read_pps_file(self.config.get_t2_pps_file_name())

class bcolors:

    # colors for info, warning and fail outputs
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class pcolors:

    # hex color codes for plots
    SYMB  = '#004c99'
    FILL  = '#e5f2ff'
    VLINE = '#004c99'
    MA    = {'MA_5': '#ff3333',
             'MA_10': '#3fc03f',
             'MA_20': '#8533ff',
             'MA_30': '#ffcc00',
             'MA_40': '#00cbcc',
             'MA_50': '#ff751a',
             'MA_60': '#ff1ab1'
         }

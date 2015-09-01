class ErrorCode():
    def __init__(self):
        self.error_code_dict = {}
        error_codes_list = open('portal/validator/error_codes.txt', 'r').read().split('\n')
        try:
            for error_codes in error_codes_list:
                self.error_code_dict[int(error_codes.split(' ', 1)[0])] = error_codes.split(' ',1)[1]
        except:
            pass
    def __getitem__(self, error_code):
        error_string = 'Error Code '+str(error_code)+': '+self.error_code_dict[error_code]
        return error_string

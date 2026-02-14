from random import choice, randint

class Password:
    __AZ = [i for i in range(65, 91)]
    __az = [i for i in range(97, 123)]
    __nums = [i for i in range(48, 58)]
    __symbols = [i for i in range(33, 48)] + [i for i in range(58, 65)]
    def __init__(self, length=10, is_AZ=True, is_az=True, is_num=True, is_symbol=True):
        self._length = length
        self._is_AZ = is_AZ
        self._is_az = is_az
        self._is_num = is_num
        self._is_symbol = is_symbol
        self._password = ''


    @property
    def length(self):
        return self._length
    @length.setter
    def length(self, value):
        try:
            value = int(value)
        except:
            raise TypeError('Length must be an integer!')
        if not (1 <= value <= 30):
            raise ValueError('Length must be between 1 and 30!')
        self._length = value

    @property
    def is_AZ(self):
        return self._is_AZ
    @is_AZ.setter
    def is_AZ(self, value):
        if not isinstance(value, bool):
            raise TypeError('Value must be an boolean!')
        self._is_AZ = value

    @property
    def is_az(self):
        return self._is_az
    @is_az.setter
    def is_az(self, value):
        if not isinstance(value, bool):
            raise TypeError('Value must be an boolean!')
        self._is_az = value

    @property
    def is_num(self):
        return self._is_num
    @is_num.setter
    def is_num(self, value):
        if not isinstance(value, bool):
            raise TypeError('Value must be an boolean!')
        self._is_num = value

    @property
    def is_symbol(self):
        return self._is_symbol
    @is_symbol.setter
    def is_symbol(self, value):
        if not isinstance(value, bool):
            raise TypeError('Value must be an boolean!')
        self._is_symbol = value

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value):
        return
    @password.deleter
    def password(self):
        return
    def generate(self):
        self._password = ''
        __set_of_symbols = []
        if self.is_AZ:
            __set_of_symbols.append(self.__class__.__AZ)
        if self.is_az:
            __set_of_symbols.append(self.__class__.__az)
        if self.is_num:
            __set_of_symbols.append(self.__class__.__nums)
        if self.is_symbol:
            __set_of_symbols.append(self.__class__.__symbols)
        for i in range(self.length):
            group = randint(0, len(__set_of_symbols) - 1)
            self._password += chr(choice(__set_of_symbols[group]))
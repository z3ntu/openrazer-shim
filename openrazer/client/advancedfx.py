import numpy as _np


class _AdvancedFx:
    def __init__(self, device):
        self._device = device
        self._matrix_dims = device._device.MatrixDimensions

        self.matrix = Frame(self._matrix_dims)

    @property
    def cols(self):
        return self._matrix_dims[1]

    @property
    def rows(self):
        return self._matrix_dims[0]

    def _draw(self, ba):
        offset = 0
        while offset + 3 < len(ba):
            row = ba[offset]
            start = ba[offset + 1]
            end = ba[offset + 2]

            row_length = ((end + 1) - start) * 3

            rgbbytes = ba[offset + 3:offset + 3 + row_length]

            # print("row: {}, start: {}, end: {}".format(row, start, end))
            # print("row_length: {}, rgbbytes len: {}".format(row_length, len(rgbbytes)))

            self._device._device.defineCustomFrame(row, start, end, rgbbytes)

            offset += row_length + 3

        self._device._device.displayCustomFrame()

    def draw(self):
        self._draw(bytes(self.matrix))


class Frame(object):
    def __init__(self, dimensions):
        self._rows, self._cols = dimensions
        self._components = 3

        self._matrix = None
        self._fb1 = None
        self.reset()

    # Index with row, col OR y, x
    def __getitem__(self, key: tuple) -> tuple:
        assert isinstance(key, tuple), "Key is not a tuple"
        assert 0 <= key[0] < self._rows, "Row out of bounds"
        assert 0 <= key[1] < self._cols, "Column out of bounds"

        return tuple(self._matrix[:, key[0], key[1]])

    # Index with row, col OR y, x
    def __setitem__(self, key: tuple, rgb: tuple):
        assert isinstance(key, tuple), "Key is not a tuple"
        assert 0 <= key[0] < self._rows, "Row out of bounds"
        assert 0 <= key[1] < self._cols, "Column out of bounds"
        assert isinstance(rgb, (list, tuple)) and len(rgb) == 3, "Value must be a tuple,list of 3 RGB components"

        self._matrix[:, key[0], key[1]] = rgb

    def __bytes__(self) -> bytes:
        return b''.join([self.row_binary(row_id) for row_id in range(0, self._rows)])

    def reset(self):
        """
        Init/Clear the matrix
        """
        if self._matrix is None:
            self._matrix = _np.zeros((self._components, self._rows, self._cols), 'uint8')
            self._fb1 = _np.copy(self._matrix)
        else:
            self._matrix.fill(0)

    def set(self, y: int, x: int, rgb: tuple):
        self.__setitem__((y, x), rgb)

    def get(self, y: int, x: int) -> list:
        return self.__getitem__((y, x))

    def row_binary(self, row_id: int) -> bytes:
        assert 0 <= row_id < self._rows, "Row out of bounds"

        start = 0
        end = self._cols - 1

        return row_id.to_bytes(1, byteorder='big') + \
               start.to_bytes(1, byteorder='big') + \
               end.to_bytes(1, byteorder='big') + \
               self._matrix[:, row_id].tobytes(order='F')

    def to_binary(self):
        return bytes(self)

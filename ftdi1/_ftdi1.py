# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes
import ctypes.util

libftdi1 = ctypes.util.find_library('ftdi1')

# if local wordsize is same as target, keep ctypes pointer function.
if ctypes.sizeof(ctypes.c_void_p) == 8:
    POINTER_T = ctypes.POINTER
else:
    # required to access _ctypes
    import _ctypes
    # Emulate a pointer class using the approriate c_int32/c_int64 type
    # The new class should have :
    # ['__module__', 'from_param', '_type_', '__dict__', '__weakref__', '__doc__']
    # but the class should be submitted to a unique instance for each base type
    # to that if A == B, POINTER_T(A) == POINTER_T(B)
    ctypes._pointer_t_type_cache = {}
    def POINTER_T(pointee):
        # a pointer should have the same length as LONG
        fake_ptr_base_type = ctypes.c_uint64 
        # specific case for c_void_p
        if pointee is None: # VOID pointer type. c_void_p.
            pointee = type(None) # ctypes.c_void_p # ctypes.c_ulong
            clsname = 'c_void'
        else:
            clsname = pointee.__name__
        if clsname in ctypes._pointer_t_type_cache:
            return ctypes._pointer_t_type_cache[clsname]
        # make template
        class _T(_ctypes._SimpleCData,):
            _type_ = 'L'
            _subtype_ = pointee
            def _sub_addr_(self):
                return self.value
            def __repr__(self):
                return '%s(%d)'%(clsname, self.value)
            def contents(self):
                raise TypeError('This is not a ctypes pointer.')
            def __init__(self, **args):
                raise TypeError('This is not a ctypes pointer. It is not instanciable.')
        _class = type('LP_%d_%s'%(8, clsname), (_T,),{}) 
        ctypes._pointer_t_type_cache[clsname] = _class
        return _class

c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 16:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*16

_libraries = {}
_libraries[libftdi1] = ctypes.CDLL(libftdi1)


class struct_timeval(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tv_sec', ctypes.c_int64),
    ('tv_usec', ctypes.c_int64),
     ]

FTDI_MAX_EEPROM_SIZE = 256 # Variable ctypes.c_int32
MAX_POWER_MILLIAMP_PER_UNIT = 2 # Variable ctypes.c_int32

# values for enumeration 'ftdi_chip_type'
TYPE_AM = 0
TYPE_BM = 1
TYPE_2232C = 2
TYPE_R = 3
TYPE_2232H = 4
TYPE_4232H = 5
TYPE_232H = 6
TYPE_230X = 7
ftdi_chip_type = ctypes.c_int # enum

# values for enumeration 'ftdi_parity_type'
NONE = 0
ODD = 1
EVEN = 2
MARK = 3
SPACE = 4
ftdi_parity_type = ctypes.c_int # enum

# values for enumeration 'ftdi_stopbits_type'
STOP_BIT_1 = 0
STOP_BIT_15 = 1
STOP_BIT_2 = 2
ftdi_stopbits_type = ctypes.c_int # enum

# values for enumeration 'ftdi_bits_type'
BITS_7 = 7
BITS_8 = 8
ftdi_bits_type = ctypes.c_int # enum

# values for enumeration 'ftdi_break_type'
BREAK_OFF = 0
BREAK_ON = 1
ftdi_break_type = ctypes.c_int # enum

# values for enumeration 'ftdi_mpsse_mode'
BITMODE_RESET = 0
BITMODE_BITBANG = 1
BITMODE_MPSSE = 2
BITMODE_SYNCBB = 4
BITMODE_MCU = 8
BITMODE_OPTO = 16
BITMODE_CBUS = 32
BITMODE_SYNCFF = 64
BITMODE_FT1284 = 128
ftdi_mpsse_mode = ctypes.c_int # enum

# values for enumeration 'ftdi_interface'
INTERFACE_ANY = 0
INTERFACE_A = 1
INTERFACE_B = 2
INTERFACE_C = 3
INTERFACE_D = 4
ftdi_interface = ctypes.c_int # enum

# values for enumeration 'ftdi_module_detach_mode'
AUTO_DETACH_SIO_MODULE = 0
DONT_DETACH_SIO_MODULE = 1
ftdi_module_detach_mode = ctypes.c_int # enum
MPSSE_WRITE_NEG = 0x01 # Variable ctypes.c_int32
MPSSE_BITMODE = 0x02 # Variable ctypes.c_int32
MPSSE_READ_NEG = 0x04 # Variable ctypes.c_int32
MPSSE_LSB = 0x08 # Variable ctypes.c_int32
MPSSE_DO_WRITE = 0x10 # Variable ctypes.c_int32
MPSSE_DO_READ = 0x20 # Variable ctypes.c_int32
MPSSE_WRITE_TMS = 0x40 # Variable ctypes.c_int32
SET_BITS_LOW = 0x80 # Variable ctypes.c_int32
SET_BITS_HIGH = 0x82 # Variable ctypes.c_int32
GET_BITS_LOW = 0x81 # Variable ctypes.c_int32
GET_BITS_HIGH = 0x83 # Variable ctypes.c_int32
LOOPBACK_START = 0x84 # Variable ctypes.c_int32
LOOPBACK_END = 0x85 # Variable ctypes.c_int32
TCK_DIVISOR = 0x86 # Variable ctypes.c_int32
DIS_DIV_5 = 0x8a # Variable ctypes.c_int32
EN_DIV_5 = 0x8b # Variable ctypes.c_int32
EN_3_PHASE = 0x8c # Variable ctypes.c_int32
DIS_3_PHASE = 0x8d # Variable ctypes.c_int32
CLK_BITS = 0x8e # Variable ctypes.c_int32
CLK_BYTES = 0x8f # Variable ctypes.c_int32
CLK_WAIT_HIGH = 0x94 # Variable ctypes.c_int32
CLK_WAIT_LOW = 0x95 # Variable ctypes.c_int32
EN_ADAPTIVE = 0x96 # Variable ctypes.c_int32
DIS_ADAPTIVE = 0x97 # Variable ctypes.c_int32
CLK_BYTES_OR_HIGH = 0x9c # Variable ctypes.c_int32
CLK_BYTES_OR_LOW = 0x9d # Variable ctypes.c_int32
DRIVE_OPEN_COLLECTOR = 0x9e # Variable ctypes.c_int32
SEND_IMMEDIATE = 0x87 # Variable ctypes.c_int32
WAIT_ON_HIGH = 0x88 # Variable ctypes.c_int32
WAIT_ON_LOW = 0x89 # Variable ctypes.c_int32
READ_SHORT = 0x90 # Variable ctypes.c_int32
READ_EXTENDED = 0x91 # Variable ctypes.c_int32
WRITE_SHORT = 0x92 # Variable ctypes.c_int32
WRITE_EXTENDED = 0x93 # Variable ctypes.c_int32
SIO_RESET = 0 # Variable ctypes.c_int32
SIO_MODEM_CTRL = 1 # Variable ctypes.c_int32
SIO_SET_FLOW_CTRL = 2 # Variable ctypes.c_int32
SIO_SET_BAUD_RATE = 3 # Variable ctypes.c_int32
SIO_SET_DATA = 4 # Variable ctypes.c_int32
SIO_RESET_REQUEST = SIO_RESET # Variable ctypes.c_int32
SIO_SET_BAUDRATE_REQUEST = SIO_SET_BAUD_RATE # Variable ctypes.c_int32
SIO_SET_DATA_REQUEST = SIO_SET_DATA # Variable ctypes.c_int32
SIO_SET_FLOW_CTRL_REQUEST = SIO_SET_FLOW_CTRL # Variable ctypes.c_int32
SIO_SET_MODEM_CTRL_REQUEST = SIO_MODEM_CTRL # Variable ctypes.c_int32
SIO_POLL_MODEM_STATUS_REQUEST = 0x05 # Variable ctypes.c_int32
SIO_SET_EVENT_CHAR_REQUEST = 0x06 # Variable ctypes.c_int32
SIO_SET_ERROR_CHAR_REQUEST = 0x07 # Variable ctypes.c_int32
SIO_SET_LATENCY_TIMER_REQUEST = 0x09 # Variable ctypes.c_int32
SIO_GET_LATENCY_TIMER_REQUEST = 0x0A # Variable ctypes.c_int32
SIO_SET_BITMODE_REQUEST = 0x0B # Variable ctypes.c_int32
SIO_READ_PINS_REQUEST = 0x0C # Variable ctypes.c_int32
SIO_READ_EEPROM_REQUEST = 0x90 # Variable ctypes.c_int32
SIO_WRITE_EEPROM_REQUEST = 0x91 # Variable ctypes.c_int32
SIO_ERASE_EEPROM_REQUEST = 0x92 # Variable ctypes.c_int32
SIO_RESET_SIO = 0 # Variable ctypes.c_int32
SIO_RESET_PURGE_RX = 1 # Variable ctypes.c_int32
SIO_RESET_PURGE_TX = 2 # Variable ctypes.c_int32
SIO_DISABLE_FLOW_CTRL = 0x0 # Variable ctypes.c_int32
SIO_RTS_CTS_HS = 256 # Variable ctypes.c_int32
SIO_DTR_DSR_HS = 512 # Variable ctypes.c_int32
SIO_XON_XOFF_HS = 1024 # Variable ctypes.c_int32
SIO_SET_DTR_MASK = 0x1 # Variable ctypes.c_int32
SIO_SET_DTR_HIGH = 257 # Variable ctypes.c_int32
SIO_SET_DTR_LOW = 256 # Variable ctypes.c_int32
SIO_SET_RTS_MASK = 0x2 # Variable ctypes.c_int32
SIO_SET_RTS_HIGH = 514 # Variable ctypes.c_int32
SIO_SET_RTS_LOW = 512 # Variable ctypes.c_int32
class struct_ftdi_transfer_control(ctypes.Structure):
    pass

class struct_ftdi_context(ctypes.Structure):
    pass

class struct_ftdi_eeprom(ctypes.Structure):
    pass

class struct_libusb_device_handle(ctypes.Structure):
    pass

class struct_libusb_context(ctypes.Structure):
    pass

struct_ftdi_context._pack_ = True # source:False
struct_ftdi_context._fields_ = [
    ('usb_ctx', POINTER_T(struct_libusb_context)),
    ('usb_dev', POINTER_T(struct_libusb_device_handle)),
    ('usb_read_timeout', ctypes.c_int32),
    ('usb_write_timeout', ctypes.c_int32),
    ('type', ftdi_chip_type),
    ('baudrate', ctypes.c_int32),
    ('bitbang_enabled', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('readbuffer', POINTER_T(ctypes.c_ubyte)),
    ('readbuffer_offset', ctypes.c_uint32),
    ('readbuffer_remaining', ctypes.c_uint32),
    ('readbuffer_chunksize', ctypes.c_uint32),
    ('writebuffer_chunksize', ctypes.c_uint32),
    ('max_packet_size', ctypes.c_uint32),
    ('interface', ctypes.c_int32),
    ('index', ctypes.c_int32),
    ('in_ep', ctypes.c_int32),
    ('out_ep', ctypes.c_int32),
    ('bitbang_mode', ctypes.c_ubyte),
    ('PADDING_1', ctypes.c_ubyte * 3),
    ('eeprom', POINTER_T(struct_ftdi_eeprom)),
    ('error_str', POINTER_T(ctypes.c_char)),
    ('module_detach_mode', ftdi_module_detach_mode),
    ('PADDING_2', ctypes.c_ubyte * 4),
]

class struct_libusb_transfer(ctypes.Structure):
    pass

struct_ftdi_transfer_control._pack_ = True # source:False
struct_ftdi_transfer_control._fields_ = [
    ('completed', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('buf', POINTER_T(ctypes.c_ubyte)),
    ('size', ctypes.c_int32),
    ('offset', ctypes.c_int32),
    ('ftdi', POINTER_T(struct_ftdi_context)),
    ('transfer', POINTER_T(struct_libusb_transfer)),
]


# values for enumeration 'ftdi_eeprom_value'
VENDOR_ID = 0
PRODUCT_ID = 1
SELF_POWERED = 2
REMOTE_WAKEUP = 3
IS_NOT_PNP = 4
SUSPEND_DBUS7 = 5
IN_IS_ISOCHRONOUS = 6
OUT_IS_ISOCHRONOUS = 7
SUSPEND_PULL_DOWNS = 8
USE_SERIAL = 9
USB_VERSION = 10
USE_USB_VERSION = 11
MAX_POWER = 12
CHANNEL_A_TYPE = 13
CHANNEL_B_TYPE = 14
CHANNEL_A_DRIVER = 15
CHANNEL_B_DRIVER = 16
CBUS_FUNCTION_0 = 17
CBUS_FUNCTION_1 = 18
CBUS_FUNCTION_2 = 19
CBUS_FUNCTION_3 = 20
CBUS_FUNCTION_4 = 21
CBUS_FUNCTION_5 = 22
CBUS_FUNCTION_6 = 23
CBUS_FUNCTION_7 = 24
CBUS_FUNCTION_8 = 25
CBUS_FUNCTION_9 = 26
HIGH_CURRENT = 27
HIGH_CURRENT_A = 28
HIGH_CURRENT_B = 29
INVERT = 30
GROUP0_DRIVE = 31
GROUP0_SCHMITT = 32
GROUP0_SLEW = 33
GROUP1_DRIVE = 34
GROUP1_SCHMITT = 35
GROUP1_SLEW = 36
GROUP2_DRIVE = 37
GROUP2_SCHMITT = 38
GROUP2_SLEW = 39
GROUP3_DRIVE = 40
GROUP3_SCHMITT = 41
GROUP3_SLEW = 42
CHIP_SIZE = 43
CHIP_TYPE = 44
POWER_SAVE = 45
CLOCK_POLARITY = 46
DATA_ORDER = 47
FLOW_CONTROL = 48
CHANNEL_C_DRIVER = 49
CHANNEL_D_DRIVER = 50
CHANNEL_A_RS485 = 51
CHANNEL_B_RS485 = 52
CHANNEL_C_RS485 = 53
CHANNEL_D_RS485 = 54
RELEASE_NUMBER = 55
EXTERNAL_OSCILLATOR = 56
USER_DATA_ADDR = 57
ftdi_eeprom_value = ctypes.c_int # enum
class struct_ftdi_device_list(ctypes.Structure):
    pass

class struct_libusb_device(ctypes.Structure):
    pass

struct_ftdi_device_list._pack_ = True # source:False
struct_ftdi_device_list._fields_ = [
    ('next', POINTER_T(struct_ftdi_device_list)),
    ('dev', POINTER_T(struct_libusb_device)),
]

FT1284_CLK_IDLE_STATE = 0x01 # Variable ctypes.c_int32
FT1284_DATA_LSB = 0x02 # Variable ctypes.c_int32
FT1284_FLOW_CONTROL = 0x04 # Variable ctypes.c_int32
POWER_SAVE_DISABLE_H = 0x80 # Variable ctypes.c_int32
USE_SERIAL_NUM = 0x08 # Variable ctypes.c_int32

# values for enumeration 'ftdi_cbus_func'
CBUS_TXDEN = 0
CBUS_PWREN = 1
CBUS_RXLED = 2
CBUS_TXLED = 3
CBUS_TXRXLED = 4
CBUS_SLEEP = 5
CBUS_CLK48 = 6
CBUS_CLK24 = 7
CBUS_CLK12 = 8
CBUS_CLK6 = 9
CBUS_IOMODE = 10
CBUS_BB_WR = 11
CBUS_BB_RD = 12
ftdi_cbus_func = ctypes.c_int # enum

# values for enumeration 'ftdi_cbush_func'
CBUSH_TRISTATE = 0
CBUSH_TXLED = 1
CBUSH_RXLED = 2
CBUSH_TXRXLED = 3
CBUSH_PWREN = 4
CBUSH_SLEEP = 5
CBUSH_DRIVE_0 = 6
CBUSH_DRIVE1 = 7
CBUSH_IOMODE = 8
CBUSH_TXDEN = 9
CBUSH_CLK30 = 10
CBUSH_CLK15 = 11
CBUSH_CLK7_5 = 12
ftdi_cbush_func = ctypes.c_int # enum

# values for enumeration 'ftdi_cbusx_func'
CBUSX_TRISTATE = 0
CBUSX_TXLED = 1
CBUSX_RXLED = 2
CBUSX_TXRXLED = 3
CBUSX_PWREN = 4
CBUSX_SLEEP = 5
CBUSX_DRIVE_0 = 6
CBUSX_DRIVE1 = 7
CBUSX_IOMODE = 8
CBUSX_TXDEN = 9
CBUSX_CLK24 = 10
CBUSX_CLK12 = 11
CBUSX_CLK6 = 12
CBUSX_BAT_DETECT = 13
CBUSX_BAT_DETECT_NEG = 14
CBUSX_I2C_TXE = 15
CBUSX_I2C_RXF = 16
CBUSX_VBUS_SENSE = 17
CBUSX_BB_WR = 18
CBUSX_BB_RD = 19
CBUSX_TIME_STAMP = 20
CBUSX_AWAKE = 21
ftdi_cbusx_func = ctypes.c_int # enum
INVERT_TXD = 0x01 # Variable ctypes.c_int32
INVERT_RXD = 0x02 # Variable ctypes.c_int32
INVERT_RTS = 0x04 # Variable ctypes.c_int32
INVERT_CTS = 0x08 # Variable ctypes.c_int32
INVERT_DTR = 0x10 # Variable ctypes.c_int32
INVERT_DSR = 0x20 # Variable ctypes.c_int32
INVERT_DCD = 0x40 # Variable ctypes.c_int32
INVERT_RI = 0x80 # Variable ctypes.c_int32
CHANNEL_IS_UART = 0x0 # Variable ctypes.c_int32
CHANNEL_IS_FIFO = 0x1 # Variable ctypes.c_int32
CHANNEL_IS_OPTO = 0x2 # Variable ctypes.c_int32
CHANNEL_IS_CPU = 0x4 # Variable ctypes.c_int32
CHANNEL_IS_FT1284 = 0x8 # Variable ctypes.c_int32
CHANNEL_IS_RS485 = 0x10 # Variable ctypes.c_int32
DRIVE_4MA = 0 # Variable ctypes.c_int32
DRIVE_8MA = 1 # Variable ctypes.c_int32
DRIVE_12MA = 2 # Variable ctypes.c_int32
DRIVE_16MA = 3 # Variable ctypes.c_int32
SLOW_SLEW = 4 # Variable ctypes.c_int32
IS_SCHMITT = 8 # Variable ctypes.c_int32
DRIVER_VCP = 0x08 # Variable ctypes.c_int32
DRIVER_VCPH = 0x10 # Variable ctypes.c_int32
USE_USB_VERSION_BIT = 0x10 # Variable ctypes.c_int32
SUSPEND_DBUS7_BIT = 0x80 # Variable ctypes.c_int32
HIGH_CURRENT_DRIVE = 0x10 # Variable ctypes.c_int32
HIGH_CURRENT_DRIVE_R = 0x04 # Variable ctypes.c_int32
class struct_size_and_time(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('totalBytes', ctypes.c_uint64),
    ('time', struct_timeval),
     ]

class struct_c__SA_FTDIProgressInfo(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('first', struct_size_and_time),
    ('prev', struct_size_and_time),
    ('current', struct_size_and_time),
    ('totalTime', ctypes.c_double),
    ('totalRate', ctypes.c_double),
    ('currentRate', ctypes.c_double),
     ]

FTDIProgressInfo = struct_c__SA_FTDIProgressInfo
FTDIStreamCallback = ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(struct_c__SA_FTDIProgressInfo), POINTER_T(None))
class struct_ftdi_version_info(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('major', ctypes.c_int32),
    ('minor', ctypes.c_int32),
    ('micro', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('version_str', POINTER_T(ctypes.c_char)),
    ('snapshot_str', POINTER_T(ctypes.c_char)),
     ]

ftdi_init = _libraries[libftdi1].ftdi_init
ftdi_init.restype = ctypes.c_int32
ftdi_init.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_new = _libraries[libftdi1].ftdi_new
ftdi_new.restype = POINTER_T(struct_ftdi_context)
ftdi_new.argtypes = []
ftdi_set_interface = _libraries[libftdi1].ftdi_set_interface
ftdi_set_interface.restype = ctypes.c_int32
ftdi_set_interface.argtypes = [POINTER_T(struct_ftdi_context), ftdi_interface]
ftdi_deinit = _libraries[libftdi1].ftdi_deinit
ftdi_deinit.restype = None
ftdi_deinit.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_free = _libraries[libftdi1].ftdi_free
ftdi_free.restype = None
ftdi_free.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_set_usbdev = _libraries[libftdi1].ftdi_set_usbdev
ftdi_set_usbdev.restype = None
ftdi_set_usbdev.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(struct_libusb_device_handle)]
ftdi_get_library_version = _libraries[libftdi1].ftdi_get_library_version
ftdi_usb_find_all = _libraries[libftdi1].ftdi_usb_find_all
ftdi_usb_find_all.restype = ctypes.c_int32
ftdi_usb_find_all.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(POINTER_T(struct_ftdi_device_list)), ctypes.c_int32, ctypes.c_int32]
ftdi_list_free = _libraries[libftdi1].ftdi_list_free
ftdi_list_free.restype = None
ftdi_list_free.argtypes = [POINTER_T(POINTER_T(struct_ftdi_device_list))]
ftdi_list_free2 = _libraries[libftdi1].ftdi_list_free2
ftdi_list_free2.restype = None
ftdi_list_free2.argtypes = [POINTER_T(struct_ftdi_device_list)]
ftdi_usb_get_strings = _libraries[libftdi1].ftdi_usb_get_strings
ftdi_usb_get_strings.restype = ctypes.c_int32
ftdi_usb_get_strings.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(struct_libusb_device), POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_char), ctypes.c_int32]
ftdi_usb_get_strings2 = _libraries[libftdi1].ftdi_usb_get_strings2
ftdi_usb_get_strings2.restype = ctypes.c_int32
ftdi_usb_get_strings2.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(struct_libusb_device), POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_char), ctypes.c_int32, POINTER_T(ctypes.c_char), ctypes.c_int32]
ftdi_eeprom_set_strings = _libraries[libftdi1].ftdi_eeprom_set_strings
ftdi_eeprom_set_strings.restype = ctypes.c_int32
ftdi_eeprom_set_strings.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
ftdi_usb_open = _libraries[libftdi1].ftdi_usb_open
ftdi_usb_open.restype = ctypes.c_int32
ftdi_usb_open.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32, ctypes.c_int32]
ftdi_usb_open_desc = _libraries[libftdi1].ftdi_usb_open_desc
ftdi_usb_open_desc.restype = ctypes.c_int32
ftdi_usb_open_desc.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32, ctypes.c_int32, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
ftdi_usb_open_desc_index = _libraries[libftdi1].ftdi_usb_open_desc_index
ftdi_usb_open_desc_index.restype = ctypes.c_int32
ftdi_usb_open_desc_index.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32, ctypes.c_int32, POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), ctypes.c_uint32]
ftdi_usb_open_dev = _libraries[libftdi1].ftdi_usb_open_dev
ftdi_usb_open_dev.restype = ctypes.c_int32
ftdi_usb_open_dev.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(struct_libusb_device)]
ftdi_usb_open_string = _libraries[libftdi1].ftdi_usb_open_string
ftdi_usb_open_string.restype = ctypes.c_int32
ftdi_usb_open_string.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_char)]
ftdi_usb_close = _libraries[libftdi1].ftdi_usb_close
ftdi_usb_close.restype = ctypes.c_int32
ftdi_usb_close.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_usb_reset = _libraries[libftdi1].ftdi_usb_reset
ftdi_usb_reset.restype = ctypes.c_int32
ftdi_usb_reset.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_usb_purge_rx_buffer = _libraries[libftdi1].ftdi_usb_purge_rx_buffer
ftdi_usb_purge_rx_buffer.restype = ctypes.c_int32
ftdi_usb_purge_rx_buffer.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_usb_purge_tx_buffer = _libraries[libftdi1].ftdi_usb_purge_tx_buffer
ftdi_usb_purge_tx_buffer.restype = ctypes.c_int32
ftdi_usb_purge_tx_buffer.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_usb_purge_buffers = _libraries[libftdi1].ftdi_usb_purge_buffers
ftdi_usb_purge_buffers.restype = ctypes.c_int32
ftdi_usb_purge_buffers.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_set_baudrate = _libraries[libftdi1].ftdi_set_baudrate
ftdi_set_baudrate.restype = ctypes.c_int32
ftdi_set_baudrate.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32]
ftdi_set_line_property = _libraries[libftdi1].ftdi_set_line_property
ftdi_set_line_property.restype = ctypes.c_int32
ftdi_set_line_property.argtypes = [POINTER_T(struct_ftdi_context), ftdi_bits_type, ftdi_stopbits_type, ftdi_parity_type]
ftdi_set_line_property2 = _libraries[libftdi1].ftdi_set_line_property2
ftdi_set_line_property2.restype = ctypes.c_int32
ftdi_set_line_property2.argtypes = [POINTER_T(struct_ftdi_context), ftdi_bits_type, ftdi_stopbits_type, ftdi_parity_type, ftdi_break_type]
ftdi_read_data = _libraries[libftdi1].ftdi_read_data
ftdi_read_data.restype = ctypes.c_int32
ftdi_read_data.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
ftdi_read_data_set_chunksize = _libraries[libftdi1].ftdi_read_data_set_chunksize
ftdi_read_data_set_chunksize.restype = ctypes.c_int32
ftdi_read_data_set_chunksize.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_uint32]
ftdi_read_data_get_chunksize = _libraries[libftdi1].ftdi_read_data_get_chunksize
ftdi_read_data_get_chunksize.restype = ctypes.c_int32
ftdi_read_data_get_chunksize.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_uint32)]
ftdi_write_data = _libraries[libftdi1].ftdi_write_data
ftdi_write_data.restype = ctypes.c_int32
ftdi_write_data.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
ftdi_write_data_set_chunksize = _libraries[libftdi1].ftdi_write_data_set_chunksize
ftdi_write_data_set_chunksize.restype = ctypes.c_int32
ftdi_write_data_set_chunksize.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_uint32]
ftdi_write_data_get_chunksize = _libraries[libftdi1].ftdi_write_data_get_chunksize
ftdi_write_data_get_chunksize.restype = ctypes.c_int32
ftdi_write_data_get_chunksize.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_uint32)]
ftdi_readstream = _libraries[libftdi1].ftdi_readstream
ftdi_readstream.restype = ctypes.c_int32
ftdi_readstream.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_ubyte), ctypes.c_int32, POINTER_T(struct_c__SA_FTDIProgressInfo), POINTER_T(None))), POINTER_T(None), ctypes.c_int32, ctypes.c_int32]
ftdi_write_data_submit = _libraries[libftdi1].ftdi_write_data_submit
ftdi_write_data_submit.restype = POINTER_T(struct_ftdi_transfer_control)
ftdi_write_data_submit.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
ftdi_read_data_submit = _libraries[libftdi1].ftdi_read_data_submit
ftdi_read_data_submit.restype = POINTER_T(struct_ftdi_transfer_control)
ftdi_read_data_submit.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
ftdi_transfer_data_done = _libraries[libftdi1].ftdi_transfer_data_done
ftdi_transfer_data_done.restype = ctypes.c_int32
ftdi_transfer_data_done.argtypes = [POINTER_T(struct_ftdi_transfer_control)]
ftdi_transfer_data_cancel = _libraries[libftdi1].ftdi_transfer_data_cancel
ftdi_transfer_data_cancel.restype = None
ftdi_transfer_data_cancel.argtypes = [POINTER_T(struct_ftdi_transfer_control), POINTER_T(struct_timeval)]
ftdi_set_bitmode = _libraries[libftdi1].ftdi_set_bitmode
ftdi_set_bitmode.restype = ctypes.c_int32
ftdi_set_bitmode.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_ubyte, ctypes.c_ubyte]
ftdi_disable_bitbang = _libraries[libftdi1].ftdi_disable_bitbang
ftdi_disable_bitbang.restype = ctypes.c_int32
ftdi_disable_bitbang.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_read_pins = _libraries[libftdi1].ftdi_read_pins
ftdi_read_pins.restype = ctypes.c_int32
ftdi_read_pins.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_ubyte)]
ftdi_set_latency_timer = _libraries[libftdi1].ftdi_set_latency_timer
ftdi_set_latency_timer.restype = ctypes.c_int32
ftdi_set_latency_timer.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_ubyte]
ftdi_get_latency_timer = _libraries[libftdi1].ftdi_get_latency_timer
ftdi_get_latency_timer.restype = ctypes.c_int32
ftdi_get_latency_timer.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_ubyte)]
ftdi_poll_modem_status = _libraries[libftdi1].ftdi_poll_modem_status
ftdi_poll_modem_status.restype = ctypes.c_int32
ftdi_poll_modem_status.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_uint16)]
ftdi_setflowctrl = _libraries[libftdi1].ftdi_setflowctrl
ftdi_setflowctrl.restype = ctypes.c_int32
ftdi_setflowctrl.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32]
ftdi_setdtr_rts = _libraries[libftdi1].ftdi_setdtr_rts
ftdi_setdtr_rts.restype = ctypes.c_int32
ftdi_setdtr_rts.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32, ctypes.c_int32]
ftdi_setdtr = _libraries[libftdi1].ftdi_setdtr
ftdi_setdtr.restype = ctypes.c_int32
ftdi_setdtr.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32]
ftdi_setrts = _libraries[libftdi1].ftdi_setrts
ftdi_setrts.restype = ctypes.c_int32
ftdi_setrts.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32]
ftdi_set_event_char = _libraries[libftdi1].ftdi_set_event_char
ftdi_set_event_char.restype = ctypes.c_int32
ftdi_set_event_char.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_ubyte, ctypes.c_ubyte]
ftdi_set_error_char = _libraries[libftdi1].ftdi_set_error_char
ftdi_set_error_char.restype = ctypes.c_int32
ftdi_set_error_char.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_ubyte, ctypes.c_ubyte]
ftdi_eeprom_initdefaults = _libraries[libftdi1].ftdi_eeprom_initdefaults
ftdi_eeprom_initdefaults.restype = ctypes.c_int32
ftdi_eeprom_initdefaults.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)]
ftdi_eeprom_build = _libraries[libftdi1].ftdi_eeprom_build
ftdi_eeprom_build.restype = ctypes.c_int32
ftdi_eeprom_build.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_eeprom_decode = _libraries[libftdi1].ftdi_eeprom_decode
ftdi_eeprom_decode.restype = ctypes.c_int32
ftdi_eeprom_decode.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32]
ftdi_get_eeprom_value = _libraries[libftdi1].ftdi_get_eeprom_value
ftdi_get_eeprom_value.restype = ctypes.c_int32
ftdi_get_eeprom_value.argtypes = [POINTER_T(struct_ftdi_context), ftdi_eeprom_value, POINTER_T(ctypes.c_int32)]
ftdi_set_eeprom_value = _libraries[libftdi1].ftdi_set_eeprom_value
ftdi_set_eeprom_value.restype = ctypes.c_int32
ftdi_set_eeprom_value.argtypes = [POINTER_T(struct_ftdi_context), ftdi_eeprom_value, ctypes.c_int32]
ftdi_get_eeprom_buf = _libraries[libftdi1].ftdi_get_eeprom_buf
ftdi_get_eeprom_buf.restype = ctypes.c_int32
ftdi_get_eeprom_buf.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
ftdi_set_eeprom_buf = _libraries[libftdi1].ftdi_set_eeprom_buf
ftdi_set_eeprom_buf.restype = ctypes.c_int32
ftdi_set_eeprom_buf.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_ubyte), ctypes.c_int32]
ftdi_set_eeprom_user_data = _libraries[libftdi1].ftdi_set_eeprom_user_data
ftdi_set_eeprom_user_data.restype = ctypes.c_int32
ftdi_set_eeprom_user_data.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_char), ctypes.c_int32]
ftdi_read_eeprom = _libraries[libftdi1].ftdi_read_eeprom
ftdi_read_eeprom.restype = ctypes.c_int32
ftdi_read_eeprom.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_read_chipid = _libraries[libftdi1].ftdi_read_chipid
ftdi_read_chipid.restype = ctypes.c_int32
ftdi_read_chipid.argtypes = [POINTER_T(struct_ftdi_context), POINTER_T(ctypes.c_uint32)]
ftdi_write_eeprom = _libraries[libftdi1].ftdi_write_eeprom
ftdi_write_eeprom.restype = ctypes.c_int32
ftdi_write_eeprom.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_erase_eeprom = _libraries[libftdi1].ftdi_erase_eeprom
ftdi_erase_eeprom.restype = ctypes.c_int32
ftdi_erase_eeprom.argtypes = [POINTER_T(struct_ftdi_context)]
ftdi_read_eeprom_location = _libraries[libftdi1].ftdi_read_eeprom_location
ftdi_read_eeprom_location.restype = ctypes.c_int32
ftdi_read_eeprom_location.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32, POINTER_T(ctypes.c_uint16)]
ftdi_write_eeprom_location = _libraries[libftdi1].ftdi_write_eeprom_location
ftdi_write_eeprom_location.restype = ctypes.c_int32
ftdi_write_eeprom_location.argtypes = [POINTER_T(struct_ftdi_context), ctypes.c_int32, ctypes.c_uint16]
ftdi_get_error_string = _libraries[libftdi1].ftdi_get_error_string
ftdi_get_error_string.restype = POINTER_T(ctypes.c_char)
ftdi_get_error_string.argtypes = [POINTER_T(struct_ftdi_context)]
__all__ = \
    ['ftdi_set_eeprom_value', 'CHANNEL_A_DRIVER', 'CBUS_TXDEN',
    'CHANNEL_C_DRIVER', 'TYPE_230X', 'CBUSX_CLK12', 'EN_ADAPTIVE',
    'CLK_WAIT_HIGH', 'BREAK_ON', 'CBUS_BB_WR', 'TYPE_2232H',
    'INVERT_RTS', 'FT1284_CLK_IDLE_STATE', 'CBUSX_VBUS_SENSE',
    'INVERT_RI', 'BREAK_OFF', 'CBUSH_CLK30',
    'ftdi_read_data_set_chunksize', 'HIGH_CURRENT_B',
    'ftdi_read_eeprom', 'CBUSH_CLK7_5', 'SIO_MODEM_CTRL',
    'DRIVE_OPEN_COLLECTOR', 'EXTERNAL_OSCILLATOR',
    'SIO_RESET_REQUEST', 'GROUP3_SLEW', 'TYPE_BM', 'INVERT_CTS',
    'ftdi_parity_type', 'MPSSE_WRITE_TMS', 'ftdi_set_interface',
    'CHANNEL_IS_OPTO', 'FTDIProgressInfo', 'DIS_DIV_5',
    'CLK_BYTES_OR_HIGH', 'MPSSE_DO_READ', 'CBUS_FUNCTION_9',
    'HIGH_CURRENT', 'RELEASE_NUMBER', 'USE_USB_VERSION',
    'CBUSH_TXDEN', 'ftdi_read_eeprom_location',
    'HIGH_CURRENT_DRIVE_R', 'CBUS_FUNCTION_3', 'FTDIStreamCallback',
    'CBUS_FUNCTION_1', 'struct_ftdi_device_list', 'ftdi_deinit',
    'CBUSX_I2C_TXE', 'ftdi_usb_get_strings', 'CHANNEL_B_TYPE',
    'ftdi_setflowctrl', 'CBUS_FUNCTION_8', 'SIO_SET_RTS_HIGH',
    'CBUS_CLK6', 'HIGH_CURRENT_DRIVE', 'CBUSX_DRIVE1',
    'ftdi_disable_bitbang', 'TYPE_2232C', 'SIO_SET_FLOW_CTRL',
    'DIS_ADAPTIVE', 'CBUSH_IOMODE', 'CHANNEL_IS_UART', 'STOP_BIT_2',
    'GROUP1_SCHMITT', 'ftdi_usb_reset', 'EN_3_PHASE',
    'ftdi_transfer_data_cancel', 'LOOPBACK_START',
    'SIO_SET_BAUDRATE_REQUEST', 'ftdi_eeprom_value',
    'CBUS_FUNCTION_7', 'WRITE_SHORT', 'CBUSX_CLK24', 'BITMODE_OPTO',
    'INTERFACE_A', 'PRODUCT_ID', 'CBUS_FUNCTION_6', 'CBUSH_DRIVE_0',
    'SLOW_SLEW', 'ftdi_read_data', 'TYPE_R', 'STOP_BIT_1',
    'SIO_SET_MODEM_CTRL_REQUEST', 'LOOPBACK_END', 'TYPE_4232H',
    'IN_IS_ISOCHRONOUS', 'SET_BITS_LOW', 'DRIVE_16MA', 'ftdi_new',
    'CBUS_BB_RD', 'ftdi_list_free', 'CHIP_TYPE', 'BITMODE_SYNCFF',
    'CBUSX_TRISTATE', 'SIO_RESET_PURGE_TX', 'SUSPEND_PULL_DOWNS',
    'MPSSE_READ_NEG', 'SIO_DTR_DSR_HS', 'struct_ftdi_version_info',
    'SIO_SET_BITMODE_REQUEST', 'struct_libusb_transfer',
    'HIGH_CURRENT_A', 'BITMODE_RESET', 'BITMODE_FT1284',
    'STOP_BIT_15', 'DONT_DETACH_SIO_MODULE', 'CBUSH_RXLED',
    'SIO_RESET', 'ftdi_setrts', 'ftdi_get_eeprom_buf',
    'ftdi_set_bitmode', 'CBUS_CLK24', 'CBUS_SLEEP', 'INVERT_DSR',
    'WAIT_ON_LOW', 'CBUS_TXRXLED', 'CHANNEL_A_RS485',
    'CHANNEL_A_TYPE', 'CHANNEL_B_RS485', 'CBUS_FUNCTION_5',
    'SUSPEND_DBUS7_BIT', 'ftdi_usb_open_string', 'WAIT_ON_HIGH',
    'ftdi_write_data_get_chunksize', 'CBUSX_BAT_DETECT_NEG',
    'OUT_IS_ISOCHRONOUS', 'CBUSH_SLEEP', 'CBUSX_PWREN', 'CLK_BYTES',
    'CBUSX_TXRXLED', 'MARK', 'IS_NOT_PNP', 'CBUSX_SLEEP',
    'FLOW_CONTROL', 'USE_SERIAL_NUM', 'CBUSX_TIME_STAMP',
    'ftdi_set_error_char', 'CLK_BYTES_OR_LOW', 'MPSSE_DO_WRITE',
    'struct_size_and_time', 'ftdi_get_eeprom_value',
    'SIO_RESET_PURGE_RX', 'INTERFACE_C', 'SIO_RTS_CTS_HS',
    'ftdi_usb_open_dev', 'INVERT_RXD', 'ftdi_setdtr',
    'ftdi_read_data_get_chunksize', 'GROUP2_DRIVE',
    'CHANNEL_IS_FT1284', 'CBUSX_I2C_RXF',
    'SIO_SET_EVENT_CHAR_REQUEST', 'struct_libusb_context',
    'USE_SERIAL', 'ftdi_set_baudrate', 'SIO_SET_BAUD_RATE',
    'CHANNEL_D_RS485', 'CHANNEL_IS_FIFO', 'ftdi_write_data_submit',
    'SIO_XON_XOFF_HS', 'CHANNEL_D_DRIVER', 'ftdi_eeprom_decode',
    'GROUP0_SCHMITT', 'GROUP0_SLEW', 'USER_DATA_ADDR', 'BITS_7',
    'SIO_RESET_SIO', 'SUSPEND_DBUS7', 'ftdi_usb_get_strings2',
    'ftdi_eeprom_build', 'SIO_GET_LATENCY_TIMER_REQUEST',
    'REMOTE_WAKEUP', 'ftdi_get_latency_timer', 'POWER_SAVE_DISABLE_H',
    'ftdi_usb_open_desc', 'SELF_POWERED', 'ftdi_set_usbdev',
    'ftdi_eeprom_set_strings', 'struct_timeval',
    'SIO_POLL_MODEM_STATUS_REQUEST', 'CLOCK_POLARITY',
    'GET_BITS_HIGH', 'READ_EXTENDED', 'SIO_SET_RTS_MASK',
    'GROUP1_SLEW', 'struct_libusb_device', 'IS_SCHMITT',
    'struct_ftdi_context', 'ftdi_usb_open_desc_index',
    'ftdi_readstream', 'ftdi_set_latency_timer',
    'SIO_READ_EEPROM_REQUEST', 'ftdi_set_eeprom_buf',
    'ftdi_eeprom_initdefaults', 'CBUS_CLK12',
    'ftdi_module_detach_mode', 'ftdi_stopbits_type',
    'CBUS_FUNCTION_2', 'ftdi_break_type', 'SEND_IMMEDIATE',
    'MAX_POWER_MILLIAMP_PER_UNIT', 'ftdi_usb_close',
    'ftdi_usb_purge_rx_buffer', 'ftdi_read_chipid', 'EVEN',
    'CBUSH_TXRXLED', 'MPSSE_WRITE_NEG', 'ftdi_free',
    'CHANNEL_IS_RS485', 'VENDOR_ID', 'CBUSX_CLK6', 'DRIVER_VCP',
    'ODD', 'NONE', 'MAX_POWER', 'FT1284_DATA_LSB', 'DIS_3_PHASE',
    'BITS_8', 'CBUSH_TRISTATE', 'MPSSE_LSB',
    'SIO_SET_FLOW_CTRL_REQUEST', 'CBUS_FUNCTION_0', 'SET_BITS_HIGH',
    'SIO_SET_DATA_REQUEST', 'SIO_READ_PINS_REQUEST',
    'CBUSX_BAT_DETECT', 'CBUS_IOMODE', 'SIO_SET_DTR_HIGH',
    'CBUSH_CLK15', 'ftdi_cbusx_func', 'POWER_SAVE', 'CBUSX_DRIVE_0',
    'GROUP2_SCHMITT', 'GROUP3_DRIVE', 'ftdi_write_data',
    'struct_ftdi_eeprom', 'GROUP3_SCHMITT', 'ftdi_transfer_data_done',
    'SIO_SET_RTS_LOW', 'ftdi_cbush_func', 'CHANNEL_B_DRIVER',
    'USE_USB_VERSION_BIT', 'BITMODE_BITBANG', 'INVERT_TXD',
    'GROUP1_DRIVE', 'INVERT', 'INVERT_DTR', 'ftdi_poll_modem_status',
    'DRIVER_VCPH', 'SIO_SET_DTR_MASK', 'SIO_SET_DTR_LOW',
    'INTERFACE_ANY', 'CBUS_FUNCTION_4', 'SIO_DISABLE_FLOW_CTRL',
    'ftdi_read_data_submit', 'CHANNEL_C_RS485', 'CLK_BITS',
    'ftdi_set_line_property', 'CBUSH_PWREN', 'ftdi_interface',
    'ftdi_mpsse_mode', 'CHIP_SIZE', 'FT1284_FLOW_CONTROL',
    'GROUP2_SLEW', 'struct_c__SA_FTDIProgressInfo',
    'SIO_ERASE_EEPROM_REQUEST', 'AUTO_DETACH_SIO_MODULE',
    'DATA_ORDER', 'CBUSH_DRIVE1', 'DRIVE_4MA',
    'ftdi_write_data_set_chunksize', 'CBUS_RXLED',
    'ftdi_usb_purge_buffers', 'CHANNEL_IS_CPU', 'ftdi_list_free2',
    'SIO_WRITE_EEPROM_REQUEST', 'CLK_WAIT_LOW', 'READ_SHORT',
    'ftdi_get_error_string', 'BITMODE_SYNCBB', 'USB_VERSION',
    'ftdi_bits_type', 'CBUSX_TXDEN', 'ftdi_usb_purge_tx_buffer',
    'SPACE', 'BITMODE_CBUS', 'WRITE_EXTENDED', 'BITMODE_MCU',
    'GET_BITS_LOW', 'ftdi_init', 'SIO_SET_DATA', 'CBUS_TXLED',
    'CBUSX_TXLED', 'ftdi_set_eeprom_user_data', 'ftdi_erase_eeprom',
    'FTDI_MAX_EEPROM_SIZE', 'MPSSE_BITMODE',
    'SIO_SET_LATENCY_TIMER_REQUEST', 'TYPE_AM',
    'ftdi_set_line_property2', 'ftdi_setdtr_rts',
    'ftdi_write_eeprom_location', 'SIO_SET_ERROR_CHAR_REQUEST',
    'CBUS_PWREN', 'ftdi_cbus_func', 'struct_libusb_device_handle',
    'INTERFACE_D', 'TCK_DIVISOR', 'CBUSX_IOMODE', 'GROUP0_DRIVE',
    'CBUSX_BB_WR', 'CBUSX_BB_RD', 'CBUSX_AWAKE', 'INVERT_DCD',
    'TYPE_232H', 'BITMODE_MPSSE', 'ftdi_usb_find_all',
    'ftdi_read_pins', 'ftdi_set_event_char', 'INTERFACE_B',
    'EN_DIV_5', 'struct_ftdi_transfer_control', 'CBUS_CLK48',
    'ftdi_chip_type', 'DRIVE_12MA', 'ftdi_write_eeprom',
    'CBUSH_TXLED', 'DRIVE_8MA', 'CBUSX_RXLED', 'ftdi_usb_open']

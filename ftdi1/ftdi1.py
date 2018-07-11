from ._ftdi1 import *
from ctypes import *

def usb_find_all(ftdi, vendor, product):
    """
    usb_find_all(context, vendor, product) -> (return_code, devlist)



    Finds all ftdi devices with given VID:PID on the usb bus. Creates a
    new ftdi_device_list which needs to be deallocated by ftdi_list_free()
    after use. With VID:PID 0:0, search for the default devices
    (0x403:0x6001, 0x403:0x6010, 0x403:0x6011, 0x403:0x6014, 0x403:0x6015)

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    devlist:  Pointer where to store list of found devices

    vendor:  Vendor ID to search for

    product:  Product ID to search for

    Returns:
    --------

    >0:  number of devices found

    -3:  out of memory

    -5:  libusb_get_device_list() failed

    -6:  libusb_get_device_descriptor() failed 
    """
    devlist = c_ptr(0)
    ret = ftdi_usb_find_all(ftdi, byref(devlist), vendor, product)
    return [ret, devlist]

def usb_get_strings(*args):
    """
    usb_get_strings(context, device) -> (return_code, manufacturer, description, serial)



    Return device ID strings from the usb device.

    The parameters manufacturer, description and serial may be NULL or
    pointer to buffers to store the fetched strings.

    Use this function only in combination with ftdi_usb_find_all() as it
    closes the internal "usb_dev" after use.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    dev:  libusb usb_dev to use

    manufacturer:  Store manufacturer string here if not NULL

    mnf_len:  Buffer size of manufacturer string

    description:  Store product description string here if not NULL

    desc_len:  Buffer size of product description string

    serial:  Store serial string here if not NULL

    serial_len:  Buffer size of serial string

    Returns:
    --------

    0:  all fine

    -1:  wrong arguments

    -4:  unable to open device

    -7:  get product manufacturer failed

    -8:  get product description failed

    -9:  get serial number failed

    -11:  libusb_get_device_descriptor() failed 
    """
    manufacturer = c_string(0)
    description = c_string(0)
    serial = c_string(0)
    ret = ftdi_usb_get_strings(ftdi, libusb, byref(manufacturer), byref(description), byref(serial))
    return [ret, manufacturer, description, serial]

def usb_get_strings2(*args):
    """
    usb_get_strings(context, device) -> (return_code, manufacturer, description, serial)



    Return device ID strings from the usb device.

    The parameters manufacturer, description and serial may be NULL or
    pointer to buffers to store the fetched strings.

    The old function ftdi_usb_get_strings() always closes the device. This
    version only closes the device if it was opened by it.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    dev:  libusb usb_dev to use

    manufacturer:  Store manufacturer string here if not NULL

    mnf_len:  Buffer size of manufacturer string

    description:  Store product description string here if not NULL

    desc_len:  Buffer size of product description string

    serial:  Store serial string here if not NULL

    serial_len:  Buffer size of serial string

    Returns:
    --------

    0:  all fine

    -1:  wrong arguments

    -4:  unable to open device

    -7:  get product manufacturer failed

    -8:  get product description failed

    -9:  get serial number failed

    -11:  libusb_get_device_descriptor() failed 
    """
    manufacturer = c_string(0)
    description = c_string(0)
    serial = c_string(0)
    ret = ftdi_usb_get_strings2(ftdi, libusb, byref(manufacturer), byref(description), byref(serial))
    return [ret, manufacturer, description, serial]

def eeprom_get_strings(*args):
    """
    usb_get_strings(context, device) -> (return_code, manufacturer, description, serial)



    Return device ID strings from the eeprom. Device needs to be
    connected.

    The parameters manufacturer, description and serial may be NULL or
    pointer to buffers to store the fetched strings.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    manufacturer:  Store manufacturer string here if not NULL

    mnf_len:  Buffer size of manufacturer string

    product:  Store product description string here if not NULL

    prod_len:  Buffer size of product description string

    serial:  Store serial string here if not NULL

    serial_len:  Buffer size of serial string

    Returns:
    --------

    0:  all fine

    -1:  ftdi context invalid

    -2:  ftdi eeprom buffer invalid 
    """
    manufacturer = c_string(0)
    product = c_string(0)
    serial = c_string(0)
    ret = ftdi1_eeprom_get_strings(ftdi, byref(manufacturer), byref(product), byref(serial))

def read_data(ftdi, buf):
    """
    read_data(context) -> (return_code, buf)



    Reads data in chunks (see ftdi_read_data_set_chunksize()) from the
    chip.

    Automatically strips the two modem status bytes transfered during
    every read.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    buf:  Buffer to store data in

    size:  Size of the buffer

    Returns:
    --------

    -666:  USB device unavailable

    <0:  error code from libusb_bulk_transfer()

    0:  no data was available

    >0:  number of bytes read 
    """
    ba = bytearray(buf) # buf means size
    ubuf = (c_ubyte * len(ba)).from_buffer(ba)
    ret = ftdi_read_data(ftdi, ubuf, len(ubuf))
    return [ret, ba]

def write_data(ftdi, buf):
    """
    write_data(context, data) -> return_code



    Writes data in chunks (see ftdi_write_data_set_chunksize()) to the
    chip

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    buf:  Buffer with the data

    size:  Size of the buffer

    Returns:
    --------

    -666:  USB device unavailable

    <0:  error code from usb_bulk_write()

    >0:  number of bytes written 
    """
    ubuf = (c_ubyte * len(buf)).from_buffer_copy(buf)
    ret = ftdi_write_data(ftdi, ubuf, len(ubuf))
    return ret

def read_data_get_chunksize(ftdi):
    """
    read_data_get_chunksize(context ftdi) -> int



    Get read buffer chunk size.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    chunksize:  Pointer to store chunk size in

    Returns:
    --------

    0:  all fine

    -1:  FTDI context invalid 
    """
    chunksize = c_int(0)
    ret = ftdi_read_data_get_chunksize(ftdi, byref(chunksize))
    return [ret, chunksize]

def write_data_get_chunksize(ftdi):
    """
    write_data_get_chunksize(context ftdi) -> int



    Get write buffer chunk size.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    chunksize:  Pointer to store chunk size in

    Returns:
    --------

    0:  all fine

    -1:  ftdi context invalid 
    """
    chunksize = c_int(0)
    ret = ftdi_write_data_get_chunksize(ftdi, byref(chunksize))
    return [ret, chunksize]

def read_pins(ftdi):
    """
    read_pins(context) -> (return_code, pins)



    Directly read pin state, circumventing the read buffer. Useful for
    bitbang mode.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    pins:  Pointer to store pins into

    Returns:
    --------

    0:  all fine

    -1:  read pins failed

    -2:  USB device unavailable 
    """
    pins = c_uchar(0)
    ret = ftdi_read_pins(ftdi, byref(pins))
    return [ret, pins]

def get_latency_timer(ftdi):
    """
    get_latency_timer(context ftdi) -> int



    Get latency timer

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    latency:  Pointer to store latency value in

    Returns:
    --------

    0:  all fine

    -1:  unable to get latency timer

    -2:  USB device unavailable 
    """
    latency = c_uchar(0)
    ret = ftdi_get_latency_timer(ftdi, byref(latency))
    return [ret, latency]

def poll_modem_status(ftdi):
    """
    poll_modem_status(context ftdi) -> int



    Poll modem status information

    This function allows the retrieve the two status bytes of the device.
    The device sends these bytes also as a header for each read access
    where they are discarded by ftdi_read_data(). The chip generates the
    two stripped status bytes in the absence of data every 40 ms.

    Layout of the first byte: B0..B3 - must be 0

    B4 Clear to send (CTS) 0 = inactive 1 = active

    B5 Data set ready (DTS) 0 = inactive 1 = active

    B6 Ring indicator (RI) 0 = inactive 1 = active

    B7 Receive line signal detect (RLSD) 0 = inactive 1 = active

    Layout of the second byte: B0 Data ready (DR)

    B1 Overrun error (OE)

    B2 Parity error (PE)

    B3 Framing error (FE)

    B4 Break interrupt (BI)

    B5 Transmitter holding register (THRE)

    B6 Transmitter empty (TEMT)

    B7 Error in RCVR FIFO

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    status:  Pointer to store status information in. Must be two bytes.

    Returns:
    --------

    0:  all fine

    -1:  unable to retrieve status information

    -2:  USB device unavailable 
    """
    status = c_ushort(0)
    ret = ftdi_poll_modem_status(ftdi, byref(status))
    return [ret, status]

def get_eeprom_value(ftdi, value_name):
    """
    get_eeprom_value(context ftdi, enum ftdi_eeprom_value value_name) -> int



    Get a value from the decoded EEPROM structure

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    value_name:  Enum of the value to query

    value:  Pointer to store read value

    Returns:
    --------

    0:  all fine

    -1:  Value doesn't exist 
    """
    value = c_int(0)
    ret = ftdi_get_eeprom_value(ftdi, value_name, byref(value))
    return [ret, value]

def get_eeprom_buf(ftdi, buf):
    """
    get_eeprom_buf(context ftdi, unsigned char * buf) -> int



    Get the read-only buffer to the binary EEPROM content

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    buf:  buffer to receive EEPROM content

    size:  Size of receiving buffer

    Returns:
    --------

    0:  All fine

    -1:  struct ftdi_contxt or ftdi_eeprom missing

    -2:  Not enough room to store eeprom 
    """
    return ftdi_get_eeprom_buf(ftdi, buf, len(buf))

def read_eeprom_location(ftdi, eeprom_addr):
    """
    read_eeprom_location(context, eeprom_addr) -> (return_code, eeprom_val)



    Read eeprom location

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    eeprom_addr:  Address of eeprom location to be read

    eeprom_val:  Pointer to store read eeprom location

    Returns:
    --------

    0:  all fine

    -1:  read failed

    -2:  USB device unavailable 
    """
    eeprom_val = c_ushort(0)
    ret = ftdi_read_eeprom_location(ftdi, eeprom_addr, byref(eeprom_val))
    return [ret, eeprom_val]

def read_chipid(ftdi):
    """
    ftdi_read_chipid(context) -> (return_code, chipid)



    Read the FTDIChip-ID from R-type devices

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    chipid:  Pointer to store FTDIChip-ID

    Returns:
    --------

    0:  all fine

    -1:  read failed

    -2:  USB device unavailable 
    """
    chipid = c_uint(0)
    ret = ftdi_read_chipid(ftdi, byref(chipid))
    return [ret, chipid]



def init(ftdi):
    """
    init(context ftdi) -> int



    Initializes a ftdi_context.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    0:  all fine

    -1:  couldn't allocate read buffer

    -2:  couldn't allocate struct buffer

    -3:  libusb_init() failed

    This should be called before all functions 
    """
    return ftdi_init(ftdi)

def new():
    """
    new() -> context



    Allocate and initialize a new ftdi_context

    a pointer to a new ftdi_context, or NULL on failure 
    """
    return ftdi_new()

def set_interface(ftdi, interface):
    """
    set_interface(context ftdi, enum ftdi_interface interface) -> int



    Open selected channels on a chip, otherwise use first channel.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    interface:  Interface to use for FT2232C/2232H/4232H chips.

    Returns:
    --------

    0:  all fine

    -1:  unknown interface

    -2:  USB device unavailable

    -3:  Device already open, interface can't be set in that state 
    """
    return ftdi_set_interface(ftdi, interface)

def deinit(ftdi):
    """
    deinit(context ftdi)



    Deinitializes a ftdi_context.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context 
    """
    return ftdi_deinit(ftdi)

def free(ftdi):
    """
    free(context ftdi)



    Deinitialize and free an ftdi_context.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context 
    """
    return ftdi_free(ftdi)

def set_usbdev(ftdi, usbdev):
    """
    set_usbdev(context ftdi, struct libusb_device_handle * usbdev)



    Use an already open libusb device.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    usb:  libusb libusb_device_handle to use 
    """
    return ftdi_set_usbdev(ftdi, usbdev)

def get_library_version():
    """
    get_library_version() -> version_info



    Get libftdi library version.

    ftdi_version_info Library version information 
    """
    return ftdi_get_library_version()

def list_free(devlist):
    """
    list_free(struct ftdi_device_list ** devlist)



    Frees a usb device list.

    Parameters:
    -----------

    devlist:  USB device list created by ftdi_usb_find_all() 
    """
    return ftdi_list_free(devlist)

def list_free2(devlist):
    """
    list_free2(device_list devlist)



    Frees a usb device list.

    Parameters:
    -----------

    devlist:  USB device list created by ftdi_usb_find_all() 
    """
    return ftdi_list_free2(devlist)

def eeprom_set_strings(ftdi, manufacturer, product, serial):
    """eeprom_set_strings(context ftdi, char * manufacturer, char * product, char * serial) -> int"""
    manufacturer_ = None
    description_ = None
    serial_ = None
    if manufacturer:
        manufacturer_ = manufacturer.encode("utf-8")
    if description:
        description_ = description.encode("utf-8")
    if serial:
        serial_ = serial.encode("utf-8")
    return ftdi_eeprom_set_strings(ftdi, manufacturer_, product_, serial_)

def usb_open(ftdi, vendor, product):
    """
    usb_open(context ftdi, int vendor, int product) -> int



    Opens the first device with a given vendor and product ids.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    vendor:  Vendor ID

    product:  Product ID

    Returns:
    --------

    same:  as ftdi_usb_open_desc() 
    """
    return ftdi_usb_open(ftdi, vendor, product)

def usb_open_desc(ftdi, vendor, product, description, serial):
    """
    usb_open_desc(context ftdi, int vendor, int product, char const * description, char const * serial) -> int



    Opens the first device with a given, vendor id, product id,
    description and serial.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    vendor:  Vendor ID

    product:  Product ID

    description:  Description to search for. Use NULL if not needed.

    serial:  Serial to search for. Use NULL if not needed.

    Returns:
    --------

    0:  all fine

    -3:  usb device not found

    -4:  unable to open device

    -5:  unable to claim device

    -6:  reset failed

    -7:  set baudrate failed

    -8:  get product description failed

    -9:  get serial number failed

    -12:  libusb_get_device_list() failed

    -13:  libusb_get_device_descriptor() failed 
    """
    description_ = None
    serial_ = None
    if description:
        description_ = description.encode("utf-8")
    if serial:
        serial_ = serial.encode("utf-8")
    return ftdi_usb_open_desc(ftdi, vendor, product, description_, serial_)

def usb_open_desc_index(ftdi, vendor, product, description, serial, index):
    """
    usb_open_desc_index(context ftdi, int vendor, int product, char const * description, char const * serial, unsigned int index) -> int



    Opens the index-th device with a given, vendor id, product id,
    description and serial.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    vendor:  Vendor ID

    product:  Product ID

    description:  Description to search for. Use NULL if not needed.

    serial:  Serial to search for. Use NULL if not needed.

    index:  Number of matching device to open if there are more than one,
    starts with 0.

    Returns:
    --------

    0:  all fine

    -1:  usb_find_busses() failed

    -2:  usb_find_devices() failed

    -3:  usb device not found

    -4:  unable to open device

    -5:  unable to claim device

    -6:  reset failed

    -7:  set baudrate failed

    -8:  get product description failed

    -9:  get serial number failed

    -10:  unable to close device

    -11:  ftdi context invalid

    -12:  libusb_get_device_list() failed 
    """
    description_ = None
    serial_ = None
    if description:
        description_ = description.encode("utf-8")
    if serial:
        serial_ = serial.encode("utf-8")
    return ftdi_usb_open_desc_index(ftdi, vendor, product, description_, serial_, index)

def usb_open_bus_addr(ftdi, bus, addr):
    """
    usb_open_bus_addr(context ftdi, uint8_t bus, uint8_t addr) -> int



    Opens the device at a given USB bus and device address.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    bus:  Bus number

    addr:  Device address

    Returns:
    --------

    0:  all fine

    -1:  usb_find_busses() failed

    -2:  usb_find_devices() failed

    -3:  usb device not found

    -4:  unable to open device

    -5:  unable to claim device

    -6:  reset failed

    -7:  set baudrate failed

    -8:  get product description failed

    -9:  get serial number failed

    -10:  unable to close device

    -11:  ftdi context invalid

    -12:  libusb_get_device_list() failed 
    """
    return ftdi_usb_open_bus_addr(ftdi, bus, addr)

def usb_open_dev(ftdi, dev):
    """
    usb_open_dev(context ftdi, struct libusb_device * dev) -> int



    Opens a ftdi device given by an usb_device.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    dev:  libusb usb_dev to use

    Returns:
    --------

    0:  all fine

    -3:  unable to config device

    -4:  unable to open device

    -5:  unable to claim device

    -6:  reset failed

    -7:  set baudrate failed

    -8:  ftdi context invalid

    -9:  libusb_get_device_descriptor() failed

    -10:  libusb_get_config_descriptor() failed

    -11:  libusb_detach_kernel_driver() failed

    -12:  libusb_get_configuration() failed 
    """
    return ftdi_usb_open_dev(ftdi, dev)

def usb_open_string(ftdi, description):
    """
    usb_open_string(context ftdi, char const * description) -> int



    Opens the ftdi-device described by a description-string. Intended to
    be used for parsing a device-description given as commandline
    argument.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    description:  NULL-terminated description-string, using this format:
    d:<devicenode> path of bus and device-node (e.g. "003/001") within
    usb device tree (usually at /proc/bus/usb/)

    i:<vendor>:<product> first device with given vendor and product id,
    ids can be decimal, octal (preceded by "0") or hex (preceded by
    "0x")

    i:<vendor>:<product>:<index> as above with index being the number of
    the device (starting with 0) if there are more than one

    s:<vendor>:<product>:<serial> first device with given vendor id,
    product id and serial string

    The description format may be extended in later versions.

    Returns:
    --------

    0:  all fine

    -2:  libusb_get_device_list() failed

    -3:  usb device not found

    -4:  unable to open device

    -5:  unable to claim device

    -6:  reset failed

    -7:  set baudrate failed

    -8:  get product description failed

    -9:  get serial number failed

    -10:  unable to close device

    -11:  illegal description format

    -12:  ftdi context invalid 
    """
    description_ = None
    if description:
        description_ = description.encode("utf-8")
    return ftdi_usb_open_string(ftdi, description_)

def usb_close(ftdi):
    """
    usb_close(context ftdi) -> int



    Closes the ftdi device. Call ftdi_deinit() if you're cleaning up.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    0:  all fine

    -1:  usb_release failed

    -3:  ftdi context invalid 
    """
    return ftdi_usb_close(ftdi)

def usb_reset(ftdi):
    """
    usb_reset(context ftdi) -> int



    Resets the ftdi device.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    0:  all fine

    -1:  FTDI reset failed

    -2:  USB device unavailable 
    """
    return ftdi_usb_reset(ftdi)

def usb_purge_rx_buffer(ftdi):
    """
    usb_purge_rx_buffer(context ftdi) -> int



    Clears the read buffer on the chip and the internal read buffer.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    0:  all fine

    -1:  read buffer purge failed

    -2:  USB device unavailable 
    """
    return ftdi_usb_purge_rx_buffer(ftdi)

def usb_purge_tx_buffer(ftdi):
    """
    usb_purge_tx_buffer(context ftdi) -> int



    Clears the write buffer on the chip.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    0:  all fine

    -1:  write buffer purge failed

    -2:  USB device unavailable 
    """
    return ftdi_usb_purge_tx_buffer(ftdi)

def usb_purge_buffers(ftdi):
    """
    usb_purge_buffers(context ftdi) -> int



    Clears the buffers on the chip and the internal read buffer.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    0:  all fine

    -1:  read buffer purge failed

    -2:  write buffer purge failed

    -3:  USB device unavailable 
    """
    return ftdi_usb_purge_buffers(ftdi)

def set_baudrate(ftdi, baudrate):
    """
    set_baudrate(context ftdi, int baudrate) -> int



    Sets the chip baud rate

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    baudrate:  baud rate to set

    Returns:
    --------

    0:  all fine

    -1:  invalid baudrate

    -2:  setting baudrate failed

    -3:  USB device unavailable 
    """
    return ftdi_set_baudrate(ftdi, baudrate)

def set_line_property(ftdi, bits, sbit, parity):
    """
    set_line_property(context ftdi, enum ftdi_bits_type bits, enum ftdi_stopbits_type sbit, enum ftdi_parity_type parity) -> int



    Set (RS232) line characteristics. The break type can only be set via
    ftdi_set_line_property2() and defaults to "off".

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    bits:  Number of bits

    sbit:  Number of stop bits

    parity:  Parity mode

    Returns:
    --------

    0:  all fine

    -1:  Setting line property failed 
    """
    return ftdi_set_line_property(ftdi, bits, sbit, parity)

def set_line_property2(ftdi, bits, sbit, parity, break_type):
    """
    set_line_property2(context ftdi, enum ftdi_bits_type bits, enum ftdi_stopbits_type sbit, enum ftdi_parity_type parity, enum ftdi_break_type break_type) -> int



    Set (RS232) line characteristics

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    bits:  Number of bits

    sbit:  Number of stop bits

    parity:  Parity mode

    break_type:  Break type

    Returns:
    --------

    0:  all fine

    -1:  Setting line property failed

    -2:  USB device unavailable 
    """
    return ftdi_set_line_property2(ftdi, bits, sbit, parity, break_type)

def read_data_set_chunksize(ftdi, chunksize):
    """
    read_data_set_chunksize(context ftdi, unsigned int chunksize) -> int



    Configure read buffer chunk size. Default is 4096.

    Automatically reallocates the buffer.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    chunksize:  Chunk size

    Returns:
    --------

    0:  all fine

    -1:  ftdi context invalid 
    """
    return ftdi_read_data_set_chunksize(ftdi, chunksize)

def write_data_set_chunksize(ftdi, chunksize):
    """
    write_data_set_chunksize(context ftdi, unsigned int chunksize) -> int



    Configure write buffer chunk size. Default is 4096.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    chunksize:  Chunk size

    Returns:
    --------

    0:  all fine

    -1:  ftdi context invalid 
    """
    return ftdi_write_data_set_chunksize(ftdi, chunksize)

def readstream(ftdi, callback, userdata, packetsPerTransfer, numTransfers):
    """readstream(context ftdi, FTDIStreamCallback * callback, void * userdata, int packetsPerTransfer, int numTransfers) -> int"""
    return ftdi_readstream(ftdi, callback, userdata, len(data), packetsPerTransfer, numTransfers)

def write_data_submit(ftdi, buf, size):
    """
    write_data_submit(context ftdi, unsigned char * buf, int size) -> transfer_control



    Writes data to the chip. Does not wait for completion of the transfer
    nor does it make sure that the transfer was successful.

    Use libusb 1.0 asynchronous API.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    buf:  Buffer with the data

    size:  Size of the buffer

    Returns:
    --------

    NULL:  Some error happens when submit transfer

    !NULL:  Pointer to a ftdi_transfer_control 
    """
    return ftdi_write_data_submit(ftdi, buf, size)

def read_data_submit(ftdi, buf, size):
    """
    read_data_submit(context ftdi, unsigned char * buf, int size) -> transfer_control



    Reads data from the chip. Does not wait for completion of the transfer
    nor does it make sure that the transfer was successful.

    Use libusb 1.0 asynchronous API.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    buf:  Buffer with the data

    size:  Size of the buffer

    Returns:
    --------

    NULL:  Some error happens when submit transfer

    !NULL:  Pointer to a ftdi_transfer_control 
    """
    return ftdi_read_data_submit(ftdi, buf, size)

def transfer_data_done(tc):
    """
    transfer_data_done(transfer_control tc) -> int



    Wait for completion of the transfer.

    Use libusb 1.0 asynchronous API.

    Parameters:
    -----------

    tc:  pointer to ftdi_transfer_control

    Returns:
    --------

    <:  0: Some error happens

    >=:  0: Data size transferred

    tc->transfer could be NULL if "(size <= ftdi->readbuffer_remaining)"
    at ftdi_read_data_submit(). Therefore, we need to check it here. 
    """
    return ftdi_transfer_data_done(tc)

def transfer_data_cancel(tc, to):
    """
    transfer_data_cancel(transfer_control tc, struct timeval * to)



    Cancel transfer and wait for completion.

    Use libusb 1.0 asynchronous API.

    Parameters:
    -----------

    tc:  pointer to ftdi_transfer_control

    to:  pointer to timeout value or NULL for infinite 
    """
    return ftdi_transfer_data_cancel(tc, to)

def set_bitmode(ftdi, bitmask, mode):
    """
    set_bitmode(context ftdi, unsigned char bitmask, unsigned char mode) -> int



    Enable/disable bitbang modes.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    bitmask:  Bitmask to configure lines. HIGH/ON value configures a line
    as output.

    mode:  Bitbang mode: use the values defined in ftdi_mpsse_mode

    Returns:
    --------

    0:  all fine

    -1:  can't enable bitbang mode

    -2:  USB device unavailable 
    """
    return ftdi_set_bitmode(ftdi, bitmask, mode)

def disable_bitbang(ftdi):
    """
    disable_bitbang(context ftdi) -> int



    Disable bitbang mode.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    0:  all fine

    -1:  can't disable bitbang mode

    -2:  USB device unavailable 
    """
    return ftdi_disable_bitbang(ftdi)

def set_latency_timer(ftdi, latency):
    """
    set_latency_timer(context ftdi, unsigned char latency) -> int



    Set latency timer

    The FTDI chip keeps data in the internal buffer for a specific amount
    of time if the buffer is not full yet to decrease load on the usb bus.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    latency:  Value between 1 and 255

    Returns:
    --------

    0:  all fine

    -1:  latency out of range

    -2:  unable to set latency timer

    -3:  USB device unavailable 
    """
    return ftdi_set_latency_timer(ftdi, latency)

def setflowctrl(ftdi, flowctrl):
    """
    setflowctrl(context ftdi, int flowctrl) -> int



    Set flowcontrol for ftdi chip

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    flowctrl:  flow control to use. should be SIO_DISABLE_FLOW_CTRL,
    SIO_RTS_CTS_HS, SIO_DTR_DSR_HS or SIO_XON_XOFF_HS

    Returns:
    --------

    0:  all fine

    -1:  set flow control failed

    -2:  USB device unavailable 
    """
    return ftdi_setflowctrl(ftdi, flowctrl)

def setdtr_rts(ftdi, dtr, rts):
    """
    setdtr_rts(context ftdi, int dtr, int rts) -> int



    Set dtr and rts line in one pass

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    dtr:  DTR state to set line to (1 or 0)

    rts:  RTS state to set line to (1 or 0)

    Returns:
    --------

    0:  all fine

    -1:  set dtr/rts failed

    -2:  USB device unavailable 
    """
    return ftdi_setdtr_rts(ftdi, dtr, rts)

def setdtr(ftdi, state):
    """
    setdtr(context ftdi, int state) -> int



    Set dtr line

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    state:  state to set line to (1 or 0)

    Returns:
    --------

    0:  all fine

    -1:  set dtr failed

    -2:  USB device unavailable 
    """
    return ftdi_setdtr(ftdi, state)

def setrts(ftdi, state):
    """
    setrts(context ftdi, int state) -> int



    Set rts line

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    state:  state to set line to (1 or 0)

    Returns:
    --------

    0:  all fine

    -1:  set rts failed

    -2:  USB device unavailable 
    """
    return ftdi_setrts(ftdi, state)

def set_event_char(ftdi, eventch, enable):
    """
    set_event_char(context ftdi, unsigned char eventch, unsigned char enable) -> int



    Set the special event character

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    eventch:  Event character

    enable:  0 to disable the event character, non-zero otherwise

    Returns:
    --------

    0:  all fine

    -1:  unable to set event character

    -2:  USB device unavailable 
    """
    return ftdi_set_event_char(ftdi, eventch, enable)

def set_error_char(ftdi, errorch, enable):
    """
    set_error_char(context ftdi, unsigned char errorch, unsigned char enable) -> int



    Set error character

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    errorch:  Error character

    enable:  0 to disable the error character, non-zero otherwise

    Returns:
    --------

    0:  all fine

    -1:  unable to set error character

    -2:  USB device unavailable 
    """
    return ftdi_set_error_char(ftdi, errorch, enable)

def eeprom_initdefaults(ftdi, manufacturer, product, serial):
    """
    eeprom_initdefaults(context ftdi, char * manufacturer, char * product, char * serial) -> int



    Init eeprom with default values for the connected device

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    manufacturer:  String to use as Manufacturer

    product:  String to use as Product description

    serial:  String to use as Serial number description

    Returns:
    --------

    0:  all fine

    -1:  No struct ftdi_context

    -2:  No struct ftdi_eeprom

    -3:  No connected device or device not yet opened 
    """
    manufacturer_ = None
    description_ = None
    serial_ = None
    if manufacturer:
        manufacturer_ = manufacturer.encode("utf-8")
    if description:
        description_ = description.encode("utf-8")
    if serial:
        serial_ = serial.encode("utf-8")
    return ftdi_eeprom_initdefaults(ftdi, manufacturer_, product_, serial_)

def eeprom_build(ftdi):
    """
    eeprom_build(context ftdi) -> int



    Build binary buffer from ftdi_eeprom structure. Output is suitable for
    ftdi_write_eeprom().

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    >=0:  size of eeprom user area in bytes

    -1:  eeprom size (128 bytes) exceeded by custom strings

    -2:  Invalid eeprom or ftdi pointer

    -3:  Invalid cbus function setting (FIXME: Not in the code?)

    -4:  Chip doesn't support invert (FIXME: Not in the code?)

    -5:  Chip doesn't support high current drive (FIXME: Not in the code?)

    -6:  No connected EEPROM or EEPROM Type unknown 
    """
    return ftdi_eeprom_build(ftdi)

def eeprom_decode(ftdi, verbose):
    """
    eeprom_decode(context ftdi, int verbose) -> int



    Decode binary EEPROM image into an ftdi_eeprom structure.

    For FT-X devices use AN_201 FT-X MTP memory Configuration to decode.

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    verbose:  Decode EEPROM on stdout

    Returns:
    --------

    0:  all fine

    -1:  something went wrong

    FIXME: How to pass size? How to handle size field in ftdi_eeprom?
    FIXME: Strings are malloc'ed here and should be freed somewhere 
    """
    return ftdi_eeprom_decode(ftdi, verbose)

def set_eeprom_value(ftdi, value_name, value):
    """
    set_eeprom_value(context ftdi, enum ftdi_eeprom_value value_name, int value) -> int



    Set a value in the decoded EEPROM Structure No parameter checking is
    performed

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    value_name:  Enum of the value to set

    value:  to set

    Returns:
    --------

    0:  all fine

    -1:  Value doesn't exist

    -2:  Value not user settable 
    """
    return ftdi_set_eeprom_value(ftdi, value_name, value)

def set_eeprom_buf(ftdi, buf, size):
    """
    set_eeprom_buf(context ftdi, unsigned char const * buf, int size) -> int



    Set the EEPROM content from the user-supplied prefilled buffer

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    buf:  buffer to read EEPROM content

    size:  Size of buffer

    Returns:
    --------

    0:  All fine

    -1:  struct ftdi_context or ftdi_eeprom or buf missing 
    """
    return ftdi_set_eeprom_buf(ftdi, buf, size)

def set_eeprom_user_data(ftdi, buf, size):
    """
    set_eeprom_user_data(context ftdi, char const * buf, int size) -> int



    Set the EEPROM user data content from the user-supplied prefilled
    buffer

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    buf:  buffer to read EEPROM user data content

    size:  Size of buffer

    Returns:
    --------

    0:  All fine

    -1:  struct ftdi_context or ftdi_eeprom or buf missing 
    """
    return ftdi_set_eeprom_user_data(ftdi, buf, size)

def read_eeprom(ftdi):
    """
    read_eeprom(context) -> (return_code, eeprom)



    Read eeprom

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    0:  all fine

    -1:  read failed

    -2:  USB device unavailable 
    """
    return ftdi_read_eeprom(ftdi)

def write_eeprom(ftdi):
    """
    write_eeprom(context ftdi) -> int



    Write eeprom

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    0:  all fine

    -1:  read failed

    -2:  USB device unavailable

    -3:  EEPROM not initialized for the connected device; 
    """
    return ftdi_write_eeprom(ftdi)

def erase_eeprom(ftdi):
    """erase_eeprom(context ftdi) -> int"""
    return ftdi_erase_eeprom(ftdi)

def write_eeprom_location(ftdi, eeprom_addr, eeprom_val):
    """
    write_eeprom_location(context ftdi, int eeprom_addr, unsigned short eeprom_val) -> int



    Write eeprom location

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    eeprom_addr:  Address of eeprom location to be written

    eeprom_val:  Value to be written

    Returns:
    --------

    0:  all fine

    -1:  write failed

    -2:  USB device unavailable

    -3:  Invalid access to checksum protected area below 0x80

    -4:  Device can't access unprotected area

    -5:  Reading chip type failed 
    """
    return ftdi_write_eeprom_location(ftdi, eeprom_addr, eeprom_val)

def get_error_string(ftdi):
    """
    get_error_string(context ftdi) -> char *



    Get string representation for last error code

    Parameters:
    -----------

    ftdi:  pointer to ftdi_context

    Returns:
    --------

    Pointer:  to error string 
    """
    errstr = ftdi_get_error_string(ftdi)
    return cast(errstr, c_char_p).value.decode('ascii')


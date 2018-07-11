from _ftdi1 import *
from ctypes import *

def init(ftdi):
  ret = ftdi_init(ftdi)
  return ret

def new():
  ret = ftdi_new()
  return ret

def set_interface(ftdi, interface):
  ret = ftdi_set_interface(ftdi, interface)
  return ret

def deinit(ftdi):
  ret = ftdi_deinit(ftdi)
  return ret

def free(ftdi):
  ret = ftdi_free(ftdi)
  return ret

def set_usbdev(ftdi, usbdev):
  ret = ftdi_set_usbdev(ftdi, usbdev)
  return ret

def get_library_version():
  ret = ftdi_get_library_version()
  return ret

def usb_find_all(ftdi, vendor, product):
  devlist = c_ptr(0)
  ret = ftdi_usb_find_all(ftdi, byref(devlist), vendor, product)
  return [ret, devlist]

def list_free(devlist):
  ret = ftdi_list_free(devlist)
  return ret

def list_free2(devlist):
  ret = ftdi_list_free2(devlist)
  return ret

def usb_get_strings(*args):
  manufacturer = c_string(0)
  description = c_string(0)
  serial = c_string(0)
  ret = ftdi_usb_get_strings(ftdi, libusb, byref(manufacturer), ctypes.byref(description), ctypes.byref(serial))
  return [ret, manufacturer, description, serial]

def usb_get_strings2(*args):
  manufacturer = c_string(0)
  description = c_string(0)
  serial = c_string(0)
  ret = ftdi_usb_get_strings2(ftdi, libusb, byref(manufacturer), ctypes.byref(description), ctypes.byref(serial))
  return [ret, manufacturer, description, serial]

def eeprom_set_strings(ftdi, manufacturer, product, serial):
  ret = ftdi_eeprom_set_strings(ftdi, manufacturer.encode("utf-8"), product.encode("utf-8"), serial.encode("utf-8"))
  return ret

def usb_open(ftdi, vendor, product):
  ret = ftdi_usb_open(ftdi, vendor, product)
  return ret

def usb_open_desc(ftdi, vendor, product, description, serial):
  desc = None
  ser = None
  if description:
    desc = description.encode("utf-8")
  if serial:
    ser = serial.encode("utf-8")
  ret = ftdi_usb_open_desc(ftdi, vendor, product, desc, ser)
  return ret

def usb_open_desc_index(ftdi, vendor, product, description, serial, index):
  desc = None
  ser = None
  if description:
    desc = description.encode("utf-8")
  if serial:
    ser = serial.encode("utf-8")
  ret = ftdi_usb_open_desc_index(ftdi, vendor, product, desc, ser, index)
  return ret

def usb_open_dev(ftdi, dev):
  ret = ftdi_usb_open_dev(ftdi, dev)
  return ret

def usb_open_string(ftdi, description):
  ret = ftdi_usb_open_string(ftdi, description.encode("utf-8"))
  return ret

def usb_close(ftdi):
  ret = ftdi_usb_close(ftdi)
  return ret

def usb_reset(ftdi):
  ret = ftdi_usb_reset(ftdi)
  return ret

def usb_purge_rx_buffer(ftdi):
  ret = ftdi_usb_purge_rx_buffer(ftdi)
  return ret

def usb_purge_tx_buffer(ftdi):
  ret = ftdi_usb_purge_tx_buffer(ftdi)
  return ret

def usb_purge_buffers(ftdi):
  ret = ftdi_usb_purge_buffers(ftdi)
  return ret

def set_baudrate(ftdi, baudrate):
  ret = ftdi_set_baudrate(ftdi, baudrate)
  return ret

def set_line_property(ftdi, bits, sbit, parity):
  ret = ftdi_set_line_property(ftdi, bits, sbit, parity)
  return ret

def set_line_property2(ftdi, bits, sbit, parity, break_type):
  ret = ftdi_set_line_property2(ftdi, bits, sbit, parity, break_type)
  return ret

def read_data(ftdi, size):
  buf = bytearray(size)
  ubuf = (c_ubyte * len(buf)).from_buffer(buf)
  ret = ftdi_read_data(ftdi, ubuf, len(ubuf))
  return [ret, buf]

def read_data_set_chunksize(ftdi, chunksize):
  ret = ftdi_read_data_set_chunksize(ftdi, chunksize)
  return ret

def read_data_get_chunksize(ftdi):
  chunksize = c_int(0)
  ret = ftdi_read_data_get_chunksize(ftdi, byref(chunksize))
  return [ret, chunksize]

def write_data(ftdi, buf):
  ubuf = (c_ubyte * len(buf)).from_buffer_copy(buf)
  ret = ftdi_write_data(ftdi, ubuf, len(ubuf))
  return ret

def write_data_set_chunksize(ftdi, chunksize):
  ret = ftdi_write_data_set_chunksize(ftdi, chunksize)
  return ret

def write_data_get_chunksize(ftdi):
  chunksize = c_int(0)
  ret = ftdi_write_data_get_chunksize(ftdi, byref(chunksize))
  return [ret, chunksize]

def readstream(ftdi, callback, userdata, packetsPerTransfer, numTransfers):
  ret = ftdi_readstream(ftdi, callback, userdata, len(data), packetsPerTransfer, numTransfers)
  return ret

def write_data_submit(ftdi, buf, size):
  ret = ftdi_write_data_submit(ftdi, buf, size)
  return ret

def read_data_submit(ftdi, buf, size):
  ret = ftdi_read_data_submit(ftdi, buf, size)
  return ret

def transfer_data_done(tc):
  ret = ftdi_transfer_data_done(tc)
  return ret

def transfer_data_cancel(tc, to):
  ret = ftdi_transfer_data_cancel(tc, to)
  return ret

def set_bitmode(ftdi, bitmask, mode):
  ret = ftdi_set_bitmode(ftdi, bitmask, mode)
  return ret

def disable_bitbang(ftdi):
  ret = ftdi_disable_bitbang(ftdi)
  return ret

def read_pins(ftdi):
  pins = c_uchar(0)
  ret = ftdi_read_pins(ftdi, byref(pins))
  return [ret, pins]

def set_latency_timer(ftdi, latency):
  ret = ftdi_set_latency_timer(ftdi, latency)
  return ret

def get_latency_timer(ftdi):
  latency = c_uchar(0)
  ret = ftdi_get_latency_timer(ftdi, byref(latency))
  return [ret, latency]

def poll_modem_status(ftdi):
  status = c_ushort(0)
  ret = ftdi_poll_modem_status(ftdi, byref(status))
  return [ret, status]

def setflowctrl(ftdi, flowctrl):
  ret = ftdi_setflowctrl(ftdi, flowctrl)
  return ret

def setdtr_rts(ftdi, dtr, rts):
  ret = ftdi_setdtr_rts(ftdi, dtr, rts)
  return ret

def setdtr(ftdi, state):
  ret = ftdi_setdtr(ftdi, state)
  return ret

def setrts(ftdi, state):
  ret = ftdi_setrts(ftdi, state)
  return ret

def set_event_char(ftdi, eventch, enable):
  ret = ftdi_set_event_char(ftdi, eventch, enable)
  return ret

def set_error_char(ftdi, errorch, enable):
  ret = ftdi_set_error_char(ftdi, errorch, enable)
  return ret

def eeprom_initdefaults(ftdi, manufacturer, product, serial):
  ret = ftdi_eeprom_initdefaults(ftdi, manufacturer.encode("utf-8"), product.encode("utf-8"), serial.encode("utf-8"))
  return ret

def eeprom_build(ftdi):
  ret = ftdi_eeprom_build(ftdi)
  return ret

def eeprom_decode(ftdi, verbose):
  ret = ftdi_eeprom_decode(ftdi, verbose)
  return ret

def get_eeprom_value(ftdi, value_name):
  value = c_int(0)
  ret = ftdi_get_eeprom_value(ftdi, value_name, byref(value))
  return [ret, value]

def set_eeprom_value(ftdi, value_name, value):
  ret = ftdi_set_eeprom_value(ftdi, value_name, value)
  return ret

def get_eeprom_buf(ftdi, buf):
  ret = ftdi_get_eeprom_buf(ftdi, buf, len(buf))
  return ret

def set_eeprom_buf(ftdi, buf, size):
  ret = ftdi_set_eeprom_buf(ftdi, buf, size)
  return ret

def set_eeprom_user_data(ftdi, buf, size):
  ret = ftdi_set_eeprom_user_data(ftdi, buf, size)
  return ret

def read_eeprom(ftdi):
  ret = ftdi_read_eeprom(ftdi)
  return ret

def read_chipid(ftdi):
  chipid = c_uint(0)
  ret = ftdi_read_chipid(ftdi, byref(chipid))
  return [ret, chipid]

def write_eeprom(ftdi):
  ret = ftdi_write_eeprom(ftdi)
  return ret

def erase_eeprom(ftdi):
  ret = ftdi_erase_eeprom(ftdi)
  return ret

def read_eeprom_location(ftdi, eeprom_addr):
  eeprom_val = c_ushort(0)
  ret = ftdi_read_eeprom_location(ftdi, eeprom_addr, byref(eeprom_val))
  return [ret, eeprom_val]

def write_eeprom_location(ftdi, eeprom_addr, eeprom_val):
  ret = ftdi_write_eeprom_location(ftdi, eeprom_addr, eeprom_val)
  return ret

def get_error_string(ftdi):
  ret = ftdi_get_error_string(ftdi)
  return cast(ret, c_char_p).value.decode('ascii')


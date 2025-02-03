## About The Project

This project implements a simple but robust message relay for late model (2025) Renpho smart scales; model ES-CS20M. Implementation is based on the [oliexdev/openScale](https://github.com/oliexdev/openScale) project; specifically [BluetoothQNScale.java](https://github.com/oliexdev/openScale/blob/master/android_app/app/src/main/java/com/health/openscale/core/bluetooth/BluetoothQNScale.java).

The message relay scans and connects to the scale. Once connected and the scale indicates that it is in a "ready" state, the weight and resistances are posted to an http endpoint specified by the user.

## Getting Started

### Prerequisites

* Python 3.10
* Python Pip

### Installation

Do the steps below to setup and run the project locally.

1. Clone the repo
2. Install requirements
   ```sh
   pip install -r requirements.txt     # For linux environments
   pip install -r requirements-win.txt # For windows environments
   ```
3. Run application
   ```sh
   python3 main.py
   ```

## Notes

A scale purchased in 2025, but still indicating it is a model ES-CS20M appears to have different Bluetooth chipset from what is expected in openScale. The GATTR characteristics have changed:

* **service: 00001800-0000-1000-8000-00805f9b34fb (Handle: 1):** Generic Access Profile
* **reading: 00002a00-0000-1000-8000-00805f9b34fb (Handle: 2):** Device Name: bytearray(b'QN-Scale')
* **service: 0000180f-0000-1000-8000-00805f9b34fb (Handle: 4):** Battery Service
* **reading: 00002a19-0000-1000-8000-00805f9b34fb (Handle: 5):** Battery Level: bytearray(b'd')
* **service: 0000180a-0000-1000-8000-00805f9b34fb (Handle: 7):** Device Information
* **reading: 00002a29-0000-1000-8000-00805f9b34fb (Handle: 8):** Manufacturer Name String: bytearray(b'Qing Niu Technology')
* **reading: 00002a26-0000-1000-8000-00805f9b34fb (Handle: 10):** Firmware Revision String: bytearray(b'V05.1')
* **reading: 00002a23-0000-1000-8000-00805f9b34fb (Handle: 12):** System ID: bytearray(b'\xda\x02f\x00\x03\xff')
* **reading: 00002a25-0000-1000-8000-00805f9b34fb (Handle: 14):** Serial Number String: bytearray(b'')
* **service: 0000fff0-0000-1000-8000-00805f9b34fb (Handle: 16):** MEASUREMENT_SERVICE
* **reading: 0000fff1-0000-1000-8000-00805f9b34fb (Handle: 17):** NOTIFICATION_CHARACTERISTIC
* **reading: 0000fff2-0000-1000-8000-00805f9b34fb (Handle: 20):** WRITE_CHARACTERISTIC
* **service: 0000ae00-0000-1000-8000-00805f9b34fb (Handle: 128):** Vendor specific
* **reading: 0000ae01-0000-1000-8000-00805f9b34fb (Handle: 129):** Vendor specific
* **reading: 0000ae02-0000-1000-8000-00805f9b34fb (Handle: 131):** Vendor specific

## License

See `LICENSE.txt` for more information.

## References

* [oliexdev/openScale](https://github.com/oliexdev/openScale)
* [BluetoothQNScale.java](https://github.com/oliexdev/openScale/blob/master/android_app/app/src/main/java/com/health/openscale/core/bluetooth/BluetoothQNScale.java)


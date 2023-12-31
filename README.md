# btc_tracker

Tracks BTC price and block height (when a new block is mined) and displays output to a screen
![20231024_182013](https://github.com/jmcmahon66/btc_tracker/assets/141964584/4d7f9e52-520a-4c05-ac7e-5f0ed60a07df)

![20231024_182056](https://github.com/jmcmahon66/btc_tracker/assets/141964584/1c071c0f-eb9f-41e2-9241-febe5289ab99)

## Compatibility

Works on Raspbian, with Raspberry Pi 7" touchcreen LED Display


## Installation

In 'Install/' directory:

```bash
./Install.sh
```
This will create a script to launch the application on Desktop,
write API key to file and install pip dependencies


## Usage

The installation will create a btc_tracker.sh script on Desktop, which can be double-clicked to launch.


## Configuration
Configuration files can be found in 'Configs/'

'config_pi.py' will be used for Raspberry Pi Platform, these values can be modified but may cause adverse effects

'update_time = 60' The API call frequency is set to every 60 seconds in the configs, this can be adjusted 
(Note that 10,000 monthly calls are allowed by coinmarketcap api free tier - update which will display used credits coming)

'api_key.py' in Configs/ will store the coinmarketcap API key for obtaining BTC price,
this can be pre-provided in the format:
```python
api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
OR will be generated by the install script when the user enters an API key


## Contributing

Contributions are welcome, please sumbit any PRs here


## License

[MIT](https://choosealicense.com/licenses/mit/)

## Donations
If you find any of these tools and scripts useful, feel free to donate

**Lightning Address:** playfulburma39@walletofsatoshi.com



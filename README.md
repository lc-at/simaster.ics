# `simaster.ics`
Small Python script to generate a calendar (.ics) file from SIMASTER courses schedule.

## Usage
### Getting the `events.json` file from SIMASTER
1. Open SIMASTER > Akademik > Jadwal Kuliah.
2. Pop up your browser's Developer Tools and go to the Network tab (or something equivalent).
3. In the SIMASTER tab, click "Jadwal Harian".
4. In the network tab of the Developer Tools, there should be a request like this.![image](https://user-images.githubusercontent.com/30001379/153825751-892829ed-8b73-4e47-a624-10117a2b01b7.png)
5. The request should have a JSON response that looks like the `example_data.json` file.
7. Copy all that response and save it somewhere (perhaps with the name `events.json`).

### Using the tool
0. Make sure that you have installed Python (>= 3.6) and `pip`
1. Install all the required packages using `pip`
```
pip install -r requirements.txt
```
3. Run the tool: `python main.py events.json`
4. If you want output it to a file: `python main.py events.json > simaster.ics`
5. You're basically done! You can use the outputted `.ics` file for Google Calendar or something similar.

## License
This small project is licensed under the MIT License.

## Contribution
Any form of contribution is highly appreciated. Feel free to contribute (or maybe even [buying me a cofffee](https://github.com/p4kl0nc4t)).

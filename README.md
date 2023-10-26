# TDT4290-Kundestyrt-Prosjekt

Repository for TDT4290 Customer Driven Project - Group 4 - 2023

## Team members

| Name                          |
| ----------------------------- |
| Bjørn Eirik Melaaen           |
| Elisabeth Krogstad Iversen    |
| Haakon Liu Selnes             |
| Mikkel Andreas Ask Guttormsen |
| Synne Frafjord Moe            |

## Supervisor

| Name              |
| ----------------- |
| Isabella Possaghi |

## Customer

| Name           |
| -------------- |
| Kshitij Sharma |

## How to run

To activate the extension, press f5 while being in a typescript file, or run the command "Debug: Start Debugging". If you need to develop the extension, you have to open a new window from the Typescript folder, and run the extension from this window.

After activation, in the window the extension is running in, press ctrl + shift + p in windows, cmd + shift + p on mac, type, then run, AI Initiated Help if you want to run with the system promting the user, or User Initiated Help if you want to run with a help button for the user to push to get help. This should activate the statusbar and give a notification that the extension is calculating a baseline.

Run main.py in the Python folder in order to have the extension actually show the cognitive load and trigger the notifications to toggle copilot. Receiving data requires the eyetracker.

## How to run tests

### Python tests

In the terminal, in the python folder, run the command python -m pytest

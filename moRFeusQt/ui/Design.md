### Design Documentation to keep sane
- [ ] Redesign main window
  - [ ] Console output should be optional 
- [ ] Design all child windows and map button and input box names
  - [ ] TCP Client window
    - [ ] Support multiple protocols
    - [ ] TCP Addresses and Ports (savable)
    - [ ] Rx Modulation 
    - [ ] Perhaps indicate success or failure of TCP message
  - [ ] TCP Server window
    - [ ] Support remote control of moRFeus and application
  - [ ] Device window
    - [ ] All device control would go here
      - [ ] Frequency
      - [ ] Current
      - [ ] Mode
      - [ ] Bias Tee
      - [ ] LCD 
      - [ ] Investigate Firmware mode (dump the firmware?)
  - [ ] Graph window
    - [ ] Support all modes (S11,X,R,|Z| and VSWR)
    - [ ] Sweep progress bar in some dialog box 
  - [ ] Extra Functions window
    - [ ] Morse code
    - [ ] Modulations
    - [ ] Custom message
  - [ ] Debug window (toggleable)
    - [ ] All program output would be here or in the console or nowhere
- [ ] Allow for a custom message to be sent by the user
- [ ] CSV file save option
- [ ] Investigate possibility of modulation support with 100ms LO dwell time 
- [ ] Save application preferences 
  - [ ] Window positions (with multi device support. . .)
  - [ ] Dont save device settings, that what our getters are for
- [ ] Properly implement an application icon


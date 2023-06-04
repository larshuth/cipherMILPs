# cipherMILPs
We are building a small framework for us to use in the analysis of the block structures of MILPs used in linear and differential cryptanalysis

### What has been done and what we plan on doing:
- [x] Modular implementation of ciphers
  - [x] Differential cryptanalysis
    - [x] AES
      - [x] Implementation
      - [x] Tests
    - [x] LBlock
      - [x] Implementation
      - [x] Tests
    - [x] Gift64
      - [x] Implementation
      - [x] Tests
  - [x] Linear cryptanalysis
    - [x] AES
      - [x] Implementation
      - [x] Tests
    - [x] LBlock
      - [x] Implementation
      - [x] Tests
    - [x] Gift64
      - [x] Implementation
      - [x] Tests

- [ ] Different approaches to the modeling
  - [ ] Model S-boxes using Convex Hull
    - [x] Original modeling (Sun et al. 2013)
    - [ ] Extension to fix mistakenly included transitions (Baksi 2020)
  - [ ] Logical condition modeling (Sun et al. 2013) 
  - [x] New MILP S-box modeling (Baksi 2020)
  - [ ] New MILP S-box modeling (Boura and Coggia 2020)
  - [ ] Extra constraints used in evaluation (Zhoui 2019)
  - [ ] Matrix-witchery (Boura and Coggia 2020)

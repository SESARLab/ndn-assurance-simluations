# NDN Assurance simulations

This repository contains the software necessary to run simulations on the NDN platform and a Certification Agent.

## Contents

- `dataset` contains the dataset of web requests used in the simulations in a csv format;
- `applications` contains the software used during the simulation, in particular the producer and consumer;
- `logs` contains the logs produced during the simulations;
- `plots` contains the plots produced by analyzing the simulations logs;
- `script` contains the Python code necessary to start the consumer and producer services, the script used to apply a missconfiguration and the scripts used for generating plots.

## Primary software components

All the software produced is available at the following links:

- [ndn-cxx](https://github.com/SESARLab/ndn-cxx/tree/paper-Security-Certification-Scheme)
- [NFD](https://github.com/SESARLab/NFD/tree/paper-Security-Certification-Scheme)
- [Certification Agent](https://github.com/SESARLab/ndn-certification-agent/tree/paper-Security-Certification-Scheme)
- [ndn-tools](https://github.com/SESARLab/ndn-tools/tree/paper-Security-Certification-Scheme)

## Software used in the simulations

The following software has been used in the simulation environment:

- [NLSR](https://github.com/SESARLab/NLSR/tree/paper-Security-Certification-Scheme)
- [PSync](https://github.com/SESARLab/psync/tree/paper-Security-Certification-Scheme)

The simulation environment can be reproduced using the [Nix](https://nixos.org/) derivation available at the following link:

- [Nixpkgs](https://github.com/SESARLab/ndn-assurance-nixpkgs/tree/paper-Security-Certification-Scheme)

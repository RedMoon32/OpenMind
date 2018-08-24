.. OpenMind documentation master file, created by
   sphinx-quickstart on Tue May  8 08:03:17 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OpenMind's documentation!
====================================
.. image:: https://readthedocs.org/projects/dpa/badge/?version=latest
   :target: http://dpa.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Introduction
============

Nowadays Digital Personal Assistants (DPA) become more and more popular. DPAs help to increase quality of life especially for elderly or disabled people. The system is designed to use the DPA as a learning platform for engineers to provide them with the opportunity to create and test their own hypothesis. The DPA is able to recognize users' commands in natural language and transform it to the set of machine commands that can be used to control different 3rd-party application. 

Instaliation
============
1. Install dependency from file requirements.txt
2. Download project `CoreNLP <https://stanfordnlp.github.io/CoreNLP/>`_
3. Install JDK 1.8 (Required for CoreNLP)
4. Make a copy of file src/configs/default_config.ini in the same folder and name it "config.ini". It allows you to change settings without conflicts with VSC.
5. Download W2V for English and put it in folder data with name "word2vect_300.bin". (Recommend `Google News W2V 300 <https://github.com/mmihaltz/word2vec-GoogleNews-vectors>`_)
6. Download  W2V for Russian and  put it in folder data with name "rusw2v.vec" (recommended `this from rusvectors <http://rusvectores.org/static/models/rusvectores4/RNC/ruscorpora_upos_skipgram_300_5_2018.vec.gz>`_)
7. Run CoreNLP
8. Run src/Main.py


Architecture
============
In project 5 moduls can be lighlited:

1. Intent processor application is responsible for handling particular user's intents
2. Language processing module provides API for natural language modules
3. Translation module translates unsupported by the DPA languages into supported one
4. Text similarity module is responsible for measurement of text equality
5. Information extraction module retrieves payload information from text


Papers
======
Open source platform Digital Personal Assistant: `https://arxiv.org/abs/1801.03650 <https://arxiv.org/abs/1801.03650>`_

Other
=====

The Digital Personal Assistant uses Yandex Translation engine.

Introduction
============

Nowadays Digital Personal Assistants (DPA) become more and more popular. DPAs help to increase quality of life especially for elderly or disabled people. The system is designed to use the DPA as a learning platform for engineers to provide them with the opportunity to create and test their own hypothesis. The DPA is able to recognize users' commands in natural language and transform it to the set of machine commands that can be used to control different 3rd-party application. 

Instruction
===========
1. Install dependency from file instal_dependenses.bat
2. Download project `CoreNLP <https://stanfordnlp.github.io/CoreNLP/>`_
3. Install JDK 1.8 (Required for CoreNLP)
4. Make copy of file src/configs/default_config.ini in the same folder and name it "config.ini". It allows you to change settings without conflicts with VSC.
5. Download W2V for English and put it in folder data with name "word2vect_300.bin"
6. Run CoreNLP
7. Run src/Main.py

Other
=====

The Digital Personal Assistant uses Yandex Translation engine.
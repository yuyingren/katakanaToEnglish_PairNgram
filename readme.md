# Transliteration of Jpanese loanwords to the English origins.

This is a project of direct transliteration from Japanese katakana words(loanwords) to their English origins.
>
The project contains:
>
* Data:
    * A list of pairs of Japanese loanwords(in katakana) and the corresponding English words.
    >
    * An English word list, which is utilized to compose the lexicon filter in the prediction model.
    >
    The paired word list is collected and composed using two open source dictionaries from the [JMdict-EDICT Dictionary Project](http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project).
    >
    The English word list is intergrited using the [CMUdict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) and the [Webster's dictionary](https://www.gutenberg.org/ebooks/673).
    >
    The paired data is splitted into train, dev and test sets and stored in the FullData folder; There is another TestData folder, which contains a small portion of the full-sized data for testing the code.


* A pair N-gram model which is trained on the training dataset.
>
    The pair N-gram model is imported from the the SIGMORPHON2020 task1 project.
    The parameters are set up for this project.

* A prediction module which is based on the prediction model in [SIGMORPHON2020 task1](https://github.com/sigmorphon/2020/tree/master/task1) project, and modified with an English lexicon filter.

* A Evaluation module which calculates and returns the WER(word error rate) and CER(character error rate) as the measure of hte model's performance.

>
Before running any program in this project, please set up the environment with this command:

>>conda env create -f environment.yml

and activate this environment with:

>>conda activate katakanaEngTrans

You can either run all programs at once by execute [RunatOnce] or run each of them by calling [modelling], [prediction], and [evaluation] seperately. 
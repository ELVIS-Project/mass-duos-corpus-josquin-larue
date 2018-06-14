# Workflow and Guidelines for Corpus Creation

**Workflow and Guidelines for symbolic file creation and conversion for the JLSDD (Josquin La Rue Secure Duo Dataset)**, by Julie E. Cumming, Cory McKay, and Jonathan Stuchbery; with input from Néstor Nápoles López, Ian Lorenz, Jason Mile, and Ichiro Fujinaga
**June 14, 2018**

For more discussion see:
Cumming, McKay, Stuchbery, and Fujinaga, “Methodologies for Creating Symbolic Corpora of Western Music before 1600,” 19th International Society for Music Information Retrieval Conference, Paris, France, 2018.

The Corpus includes all the duos from securely attributed Masses by Josquin Desprez and Pierre de La Rue; the duos are preceded and followed by double bars (or equivalent in original notation) in the Masses, so they function as self-contained sections. Many of these duos circulated as independent pieces in duo collections of the 16th century. 

## Workflow for Corpus Creation
1. Choose a single score-editing software (same version and operating system); make sure everyone working on the project uses this version
  * We used Sibelius 8.7 for Mac
2. Use a uniform and concise file-naming convention using ASCII characters, if possible, since archiving or moving files between computers or network locations can cause problems with long file names or non-ASCII characters
3. File names should include the composer, the piece, and other relevant information for the specific research program (we distinguished between pieces with secure attributions to Josquin and La Rue and not-secure attributions, and included that information in the file names)
4. Encode provenance information and other relevant metadata in the files, in case encapsulating databases, etc. are lost; use rich characters when permitted
5. Create Templates (see below for specific recommendations for Templates)
6. Locate existing symbolic files of the desired work for the corpus (from symbolic score corpora such as the JRP [Josquin Research Project] or the CPDL [Choral Public Domain Library])
  * We searched the Masses on the JRP for self-contained duos, downloaded the Music XML files for the relevant movements from the Masses, opened them in Sibelius, and extracted the duos 
7. Transcribe or use an OMR program to produce files not available in symbolic format, using the appropriate Template and following the “Guidelines for notation” below
  * We transcribed the duos not available in the JRP from the La Rue Opera Omnia in Sibelius, and converted them so that the note durations would correspond to original note values
8. Copy each symbolic file into the appropriate Template, and make any other necessary corrections (see below for the “Guidelines for notation” below)
9. Generate PDFs of the Duos from Sibelius
10. Check the PDFs of the Sibelius files for musical or notational mistakes (in some cases this means checking them against a modern edition or an original source); correct any errors
11. Once you have all the desired pieces in corrected Sibelius files, generate MIDI files of all the duos using a script (we used the Sibelius scripting language, ManuScript), and use jSymbolic (version 2.2, in our case) to check them for inconsistencies (such as inconsistent or inappropriate tempos, dynamics, rhythmic variations, instrumentation specifications or time-signature changes) 
12. For any problematic files detected in the step above, correct the corresponding Sibelius files.
13. This corrected set of Sibelius files is the “Master Corpus.” 
Generate versions of the corpus in a range of different symbolic formats (such as Music XML, MIDI, MEI, and `**kern`). Generate each of these at the same time directly from the Sibelius files comprising the Master Corpus using a script, for maximum consistency. Humdrum (`**kern` files) cannot be generated directly from Sibelius; they can be generated from the resulting Music XML or MEI files, using Craig Sapp’s humlib (https://github.com/craigsapp/humlib)
14. If any additional problems are found with any of these files, then the Master Corpus files should be corrected, and a new set of files should be generated from them
15. Do not take a file that has been exported to another format, open it in Sibelius, and then insert that file into the Sibelius Master Corpus; this is likely to distort or transform the file


## Guidelines for Templates, for encoding consistency
* Templates are Sibelius files holding only a single blank measure
* Create a Template for each of the different clef configurations, to ensure that the transposing treble clef results in the correct octave
* The Template should include a different name for each part (e.g. “Tenor I” and “Tenor II,” rather than “Tenor,” and  “Tenor”); if two parts have the same name this can cause problems for analysis software
* Provide the most likely time signature (2/1 for duple meter; 3/1 for triple-meter sections)
* There are no tempo markings in the original sources or in modern editions, so we have chosen whole note = 80 BPM (quarter note = 320 BPM); a reasonable tempo for the performance of Renaissance music
* If you plan to generate MIDI files from the Master Corpus, make sure that the playback settings are consistent for all pieces, by including the settings in the Template
  * Use MIDI Type 1
  * Conform to General MIDI instruments
  * Avoid keyboard instruments for non-keyboard parts, as keyboard encodings can sometimes cause individual voices in a polyphonic work to be collapsed into one part
  * Standardize to 960 PPQN (Pulse Per Quarter Note)
  * Disable rubato, swing, and “human playback” settings so that encodings are as rhythmically quantized as possible, and that there is no variation in dynamics
  * To ensure consistency for playback settings in Sibelius we did the following:
    * Under File > Export > MIDI > Sounds, choose “A different playback device” and choose “General MIDI” from the dialogue option
    * Go to Play > Setup > Configuration and choose General MIDI (we used General MIDI Patch 53, voice)
    * Check in “Manual Sound Sets” that General MIDI is chosen for the Sound Set 
    * Under Play, uncheck Live Tempo and Live Playback 
    * Under Play > Interpretation > Performance > Style > Espressivo and Rubato, set to “Meccanico” 

## Guidelines for notation, for music c. 1450 to c. 1550
* Heading in score: Composer, title, source of file, as well as other relevant information, depending on the research project (so that the piece can be identified from the PDF)
* Transcription is in modern notation, in score, with time signatures, barlines, and ties
* Modern clefs: Treble clef, transposing treble clef (an octave lower, with a small “8” below the clef), bass clef
* Original notated pitch of the work
* Do not include editorial accidentals (also known as musica ficta; normally shown above the staff); remove the editorial accidentals from symbolic files
* Original note values
* The time signature is normally 2/1 for duple meter; 3/1 for triple-meter sections (though other time signatures are sometimes called for); make sure the time signature matches the number of beats in the measure
  * No time signature changes unless there is a real change of meter/mensuration in the piece 
  * When possible, make all the voices change time signatures at the same time
* The final long (“long” is the note value of the last note in almost all music before 1600) should normally be two breves, tied over the barline
  * If the final long begins in the middle of a measure, then it should be a semibreve tied to a breve tied to a breve
* Only include fermatas found in the original source (omit fermatas shown in square brackets in the modern edition); use the Sibelius symbol for the fermata that does not change the value of the note
* Correct and consistent encoding that works with the analysis software tools used in the research is more important than the appearance of the score, and more important than graphic features of the modern edition or the original notation (e.g. do not try to include original mensuration signs, ligature brackets, ranges, and incipits indicating the original clefs and note shapes)


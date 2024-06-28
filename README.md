# Powerpoint Karaoke (PK)

## Overview

This tool aims to provide a randomized slide deck when invoked.  It will read from a 
database (or a master slide deck of many available slides) and randomly choose
5-10 slides and place them in a new presentation.

During the creation, the user can select topics to be included.  A steady database
of "alternate" or out-of-context slides will be accessed to spice up the new
presentation.

Currently, Libre Office documents are being used during development.  The goal is to 
create a CLI tool that can be invoked to create the desired slide deck from scratch. This
tool could be modified to have a gui front-end, and if I can figure out how to
store slides as database objects, then we should be able to place it inside a
web framework such as Django or T3/Next.js.

## Current Status

6/28/2024: Still in the exploratory stage.  I have been successful at parsing the XML 
of the .odp document, saving a slide or "page" as a separate file, then importing that 
file into a .odp document.  For example, testPresentation.odp is modified from 5 slides 
to 6 slides when "workOnODP.py" is run.

## Background

A teaching tool I have used in the past is Powerpoint Karaoke, where
the presenter/student is tasked with providing an informative and relevant presentation
about our topic (computer science, in our case).  The presentation is usually no longer
than 5-10 slides, and the time limit is generally set at 6-10 minutes.  The
kicker is that the presenter has never seen the slide deck before!

Within a safe and fun-embracing atmosphere, students enjoy trying their best, aware that
their information might fall short or be completely wrong.  I have found that students
tend to remember the things they got wrong and were corrected than when they guessed and
happily got it right.

To make the situation more light-hearted, a random slide or two should be introduced, something
that appears to be wildly off-topic.  I have recruited other teachers from my school to provide
their slide decks.  It is more useful if the students just may have seen the slides
already, in the context of the other class.  When they realize they are looking at
something they may have already seen in Biology, this is the point when the presentation
becomes "fun" and not simple information regurgitation. 

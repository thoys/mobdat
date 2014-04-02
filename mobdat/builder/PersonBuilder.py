#!/usr/bin/env python
"""
Copyright (c) 2014, Intel Corporation

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer. 

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution. 

* Neither the name of Intel Corporation nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 

@file    PersonBuilder.py
@author  Mic Bowman
@date    2014-02-04

This file defines routines used to build profiles for people and places.

"""

import os, sys, warnings, copy

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.PersonInfo import PersonInfo
from mobdat.common.Person import *
from mobdat.common.Location import *

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class PersonBuilder(PersonInfo) :

    # -----------------------------------------------------------------
    def __init__(self) :
        PersonInfo.__init__(self)

    # -----------------------------------------------------------------
    def AddPersonProfile(self, name) :
        self.PersonProfiles[name] = PersonProfile(name)

    # -----------------------------------------------------------------
    def AddResidentialLocationProfile(self, name, residents) :
        self.ResidentialLocationProfiles[name] = ResidentialLocationProfile(name, residents)

    # -----------------------------------------------------------------
    def AddResidentialLocation(self, capsule, profile) :
        self.ResidentialLocations[capsule.Name] = ResidentialLocation(capsule, profile)

    # -----------------------------------------------------------------
    def PlacePerson(self, person) :
        bestloc = None
        bestfit = 0
        for residence in self.ResidentialLocations.itervalues() :
            fitness = residence.Fitness(person)
            if fitness > bestfit :
                bestfit = fitness
                bestloc = residence

        if bestloc :
            person.Residence = bestloc.AddPerson(person)
            self.PersonList[person.Name] = person

        return bestloc
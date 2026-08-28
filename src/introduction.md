# Introduction

> Verified against **Minecraft 26.2**

This is documentation of how Java Minecraft *works* — its systems, the data
they own, when they run, and how they talk to each other — for the current
version of the game and no other. It is the written half of a lecture
series; each chapter is one lecture's notes and follows one scenario through
the codebase.

Three things to know before reading:

- **Names, never code.** Chapters name classes, methods and packages so
  that anyone with the decompiled source can find them in a minute. They do
  not reproduce the source. If you need the code, decompile the game.
- **Mojang's names.** The identifiers here are Mojang's official mappings,
  which the decompiled source uses. Fabric's Yarn mappings differ; where a
  modder would not recognise a class under its official name, the Yarn name
  is noted once.
- **Verified.** Every backticked identifier in every chapter is checked
  against the stated version's decompile before publishing. When a new
  version lands, chapters are re-verified and the header updated; there are
  no version-difference sections.

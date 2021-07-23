#!/usr/bin/env python3

from eliza.elizamain import ElizaMain

if __name__ == "__main__":
	eliza = ElizaMain()
	with open("scripts/original1966.txt") as f:
		eliza.read_script(f)
	eliza.run_program()
run:
	unzip 21111006-qrels
	unzip 21111006-ir-systems
	cd 21111006-ir-systems && sh test.sh $(filename)

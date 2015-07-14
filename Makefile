# `adocker` is alias to `azk docker`
all:
	adocker build -t azukiapp/deploy-do latest

no-cache:
	adocker build --rm --no-cache -t azukiapp/deploy-do latest

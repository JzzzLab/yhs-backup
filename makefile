JS = js/
CSS = css/
SRC = src/
F_MF = makefile
G_IGN = .gitignore
INDEX = index.html

msg = renew
RMDIR = rm -rfv
INIT_MSG = First commit
GH_MSG = First commit: branch 'gh-pages'
MASTER_MSG = First commit: branch 'master'
REPO = git@github.com:JzzzLab/yhs-backup.git

.SILENT: all
all:
	python ./main.py

.PHONY: init
init:
	git init
	git checkout -b gh-pages
	git add .
	git commit -m "$(INIT_MSG)"
	git remote add origin $(REPO)
	git push -u origin gh-pages

.PHONY: testinit
testinit:
	git init

	git add "$(G_IGN)"
	git add "$(F_MF)"
	git add "$(CSS)"
	git add "$(JS)"
	git add "$(SRC)"
	git commit -m "$(INIT_MSG)"

	git checkout -b gh-pages
	git add "$(INDEX)"
	git commit -m "$(GH_MSG)"

	git checkout master
	git add -A
	git commit -m "$(MASTER_MSG)"

	git remote add origin $(REPO)
	git push -u origin master
	git push -u origin gh-pages

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: rmgitdir
rmgitdir:
	$(RMDIR) .git/

#make gitcp msg="commit msg"
.PHONY: gitcp
gitcp:
	git add -A
	git commit -m "$(msg)"
	git push

.PHONY: tree
tree:
	#cmd //c tree //A //F //D > tree.tmp	# WIN 10
	tree -a --dirsfirst > tree.tmp
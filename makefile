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

.SILENT: run
run:
	python ./main.py

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: gitEnv
gitEnv:
	userName=$(git log -1 --format='%an')
	userMail=$(git log -1 --format='%ae')
	git config --global user.name ${userName}
	git config --global user.email ${userMail}

.PHONY: deploy
deploy:
	headid=$(git rev-parse --short HEAD)
	git add -A
	git diff-index --quiet HEAD || git commit -m "${headid} commits $(date +%F) pages"
	git push

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
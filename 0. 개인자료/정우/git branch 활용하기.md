### 상황 1. fast-foward

1. feature/test branch 생성 및 이동

```bash
$ git checkout -b feature/test
Switched to a new branch 'feature/test'
 
```




2. 작업 완료 후 commit

```bash
$ git commit -m 'update hello.html'
[feature/test (root-commit) ec6f096] update hello.html
 2 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 hello.css
 create mode 100644 hello.html

```




3. master 이동

```bash
$ git checkout master

```




4. master에 병합

```bash
git merge feature/test
```




5. 결과 -> fast-foward (단순히 HEAD를 이동)



6. branch 삭제

```bash
$ git branch -d feature/test
```



---

### 상황 2. merge commit

1. feature/signout branch 생성 및 이동

   ```bash
   $ git checkout -b feature/signout
   ```

   

2. 작업 완료 후 commit

```bash
$ git commit -m 'add something'
```



3. master 이동

```bash
$ git checkout master

```



4. *master에 추가 commit 이 발생시키기!!*

```bash
$ touch aa.txt
$ git add .
$ git commit -m '~'
```



5. master에 병합

```bash
$ git merge feature/signout
```



6. 결과 -> 자동으로 *merge commit 발생*



7. 그래프 확인하기

```bash
$ git log --oneline --graph
```



8. branch 삭제

```bash
$ git branch -d feature/signout
```



---

### 상황 3. merge commit 충돌

1. feature/board branch 생성 및 이동

   ```bash
   $ git checkout -b feature/board
   Switched to a new branch 'feature/board'
   
   ```

   

2. 작업 완료 후 commit

```bash
$ git commit -m 'update hello.html'
[feature/board (root-commit) 973fbac] update hello.html
 2 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 hello.css
 create mode 100644 hello.html

```




3. master 이동


4. *master에 추가 commit 이 발생시키기!!*


5. master에 병합


6. 결과 -> *merge conflict발생*


7. 충돌 확인 및 해결


8. merge commit 진행

    ```bash
    $ git commit
    ```

9. 그래프 확인하기


10. branch 삭제





##되돌리기

reset : 해당 커밋 이력으로 돌아감.

revert : 해당 커밋 시점으로 돌아가는 커밋을 남김

stash : 지금 작업하는 것들을 특정한 공간에 던져두고  stash pop을 통해 꺼내서 다시 작업이 가능하다.

``` bash
$ git stash
$ git stash list
$ git stash apply #반영하기
$ git stash drop # 목록에서 지우기
$ git stash pop # apply + drop
```


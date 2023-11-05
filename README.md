# big-data-analysis
big-data-analysis

## github

 * git config --global --list
 * git config --global credential.helper store
   * ~/.git-credentials 경로에 저장
 * git rm --cached config.py
   * caching 목록 제거 

## 명령어 관련
 * nohup command > logfile 2>&1 &
	- stderr > stdout, 표준에러도 표준출력으로 리다이렉트시킴

## AWS 관련
 * IAM 설정
   1. pip install awscli
   2. aws configure
   3. aws sts get-caller-identity

## 2023-09-27

 * openSearch shcema 정의
 * 저번주에는 SQS에 크롤링한 데이터를 넣었음
 * 이번주에는 SQS에 데이터를 넣고 빼서 OpenSearch에 쓸거임
 * 과제 
   * 

## 2023-10-22

  * jupyter nbconvert --to html /Your notebook path/file.ipynb (to html)
## 2023-10-25 (9주차)
  * 사전 설치 파일 
    * 도커, 파이토치, 노em
  * 대상 파일은 아래 두 개
    * hugging_face
    * add_sentiments

## 2023-11-01 (10주차)
  * serverless
    * 생성: serverless create --template aws-python3 --name news-api-server --path news-api-server
    * 실행(로컬): serverless invoke local -f hello
    * serverless invoke local -f news_trends -p mocks/news_trends.json

  * ec2 위에서 aws configure 설정 해주고,
    * serverless deploy 
      * 도커 설정을 넣어줬기 때문에
      * 람다는 이제 가상 머신을 실행시켜 줌
      * 이전에는 Pandas 같은 파이썬 기본 패키지가 아닌게 없었기 떄문에 실행 오류가 발생했었는데
      * 그래서 해당 라이브러리를 포함한 가상 머신을 올려 실행 시켜주는 것음
    * Docker 컨테이너 생성
      * conda env list
      * conda activate news-api
      * pip install requests pandas python-dotenv
      * npm init
      * npm install --save serverless-python-requirements
      * No space left on device > export TMPDIR=$HOME/new/tmp/dir


# OMC_Project<br/>(오메추 - 오늘의 메뉴 추천~)
*※ 기존에 수행한 https://github.com/choiwanmin/OMC_project 프로젝트를 정비 및 정리*

## 목차
 * [프로젝트 소개](#프로젝트-소개)
 * [기술 스택](#기술-스택)
 * [주요 기능](#주요-기능)
 * [주요 작업 내용](#주요-작업-내용)
 * [프로젝트 아키텍쳐](#프로젝트-아키텍쳐)
 * [클라이언트 화면 UI](#클라이언트-화면-UI)
 * [기대효과](#기대효과)
 * [추후 개선사항](#추후-개선사항)
 * [기타](#기타)

## 프로젝트 소개
> ### 프로젝트 개요
 * 사용자의 재료를 기반한 레시피 큐레이팅 서비스
 * 개발 기간 : 2022.12 ~ 2023.01 (약 7주간)
 * 개발 구성원 : 5명 (FullStack 2명, BE 1명, FE 1명, DBA 1명 - 구성원 중 알고리즘 구현 3명)
> ### 프로젝트 목표
 * 팀 및 서비스 목표
   * 사용자가 입력한 재료를 최대한 활용한 레시피 추천 및 다양한 종류의 요리를 추천하고자 함
   * 서비스 타겟은 요리에 대한 지식이 부족한 사용자,<br>특히 그 중 평균적으로 요리 경험이 부족한 2030세대를 비롯한 1인가구

## 기술 스택
|구분|사용 기술|
|:---|:---|
|Front-End|`HTML`, `CSS`, `Javascript`, `Bootstrap`|
|Back-End|`python(3.8.10)`, `django(4.1.4)`, `beautifulsoup4(4.11.1)`|
|Data Analysis|`Pandas`, `Numpy`, `Matplotlib`|
|DBMS|`AWS RDS(MySQL)`|
|Storage|`AWS S3`|
|Server|`AWS EC2(Ubuntu)`, `Nginx-Gunicorn`|
|IDE|`VS code`, `Vim`, `DBeaver`, `cmder`, `Google Colaboratory`|
|SCM|`Git & Github`|
|Etc.|`Notion`, `Slack`, `Google Drive`|

## 주요 기능
* 회원가입 및 로그인
* 나만의 냉장고(사용자 재료 등록 및 삭제)
* 레시피 추천
* 나만의 냉장고 기반 레시피 추천

## 주요 작업 내용
> ### 데이터 수집
 * 만개의레시피에서 데이터 크롤링을 진행함
 * 만개의레시피는 사용자 관점 데이터가 필요한 우리 프로젝트에 적합해 보였고,<br>레시피 데이터가 정형화되어 있어 데이터 수집을 용이하게 할 수 있다는 장점이 있었음
 * 그 외에 82cook은 레시피 공유보다는 요리 커뮤니티의 성격이 강했고, 네이버 블로그 같은 곳에서<br>가져오는 레시피는 일정한 기재 패턴이 존재하지 않아 데이터 수집에 부적합하다고 판단

> ### 추천 알고리즘
#### 알고리즘 구현
 * TF-IDF
 * One-Hot Encoding
 * Helmert Encoding
 * 위 3가지 방식을 통해 레시피가 가지고 있는 재료 데이터를 모두 벡터화함 또한 사용자의 입력 재료도 벡터화함
 
 |![image](https://user-images.githubusercontent.com/24910571/218041578-f5c456e2-18a0-4421-94c2-e2272b0efb0a.png)|
 |:--:|
 |위처럼 벡터화된 입력 데이터와 레시피 데이터를 cos similiraty 계산을 통해 유사한 레시피를 추천해줌|

#### 성능평가
 * 성능은 재료의 일치도를 기준으로 평가하였음<br>(사용자가 입력한 냉장고 재료를 가장 많이 사용하는 방식이 좋은 방식이라고 생각)

 |![image](https://user-images.githubusercontent.com/24910571/218041734-3be9c58c-6ec4-4a2b-8596-e0b6bd9531a1.png)|
 |:--:|
 |우리가 가지고 있는 재료들 중 랜덤하게 표본을 각 1000세트씩 추출하여 성능평가를 돌려보았음.<br>One-Hot 인코딩 방식이 성능이 그나마 좋게 나오는 것을 확인|
 
 |![image](https://user-images.githubusercontent.com/24910571/218041747-dac4ad04-b984-4ddb-9fc7-7737ee0dbf97.png)|
 |:--:|
 |위의 랜덤 표본은 재료들 간 유사도가 낮다고 생각하여 우리가 가지고 있는<br>레시피 재료 세트 중 임의로 1000세트를 뽑아 성능평가를 진행하였음|
 
 * 그래도 One-Hot 인코딩 방식이 일치도가 높게 나와 서비스에는 해당 인코딩 방식을 사용하는 것으로 채택

## 프로젝트 아키텍쳐
|![image](https://user-images.githubusercontent.com/24910571/218040503-db638de6-4452-4762-a0c5-9482e34f55f4.png)|
|:--:|

## 클라이언트 화면 UI
*※ 2023/01/31 기준 데이터 UI*

> ### 메인 관련 페이지

<details>
<summary>메인 관련 페이지 보기</summary>
<div markdown="1">
 
 |메인|
 |:---:|
 |![pd_omcpjt_ui (2)](https://github.com/user-attachments/assets/bc0b4b07-a07f-40c5-996b-faf9868e6ba6)|

 |오늘의 메뉴 추천|오늘의 메뉴 추천<br/>(봄 인기 레시피)|오늘의 메뉴 추천<br/>(아이 인기 레시피)|
 |:---:|:---:|:---:|
 |![pd_omcpjt_ui (4)](https://github.com/user-attachments/assets/dc067c8a-88bd-401c-9675-43312094bd86)|![pd_omcpjt_ui (5)](https://github.com/user-attachments/assets/83c47364-ccc3-40f1-ab45-5dc6b87eef95)|![pd_omcpjt_ui (3)](https://github.com/user-attachments/assets/efbad051-af5e-4b2b-9fec-734ad35c5e2b)|

 |회원가입<br/>페이지 이동|회원가입 페이지|로그인 페이지|로그인 후<br/>페이지|
 |:---:|:---:|:---:|:---:|
 |![pd_omcpjt_ui (7)](https://github.com/user-attachments/assets/0d8e08d2-c674-4d3a-b591-73419d9434f0)|![pd_omcpjt_ui (9)](https://github.com/user-attachments/assets/0568fac7-afe5-400e-a727-94753a92cb5c)|![pd_omcpjt_ui (10)](https://github.com/user-attachments/assets/c976a98d-5a19-4c71-b761-a8d0c8f19018)|![pd_omcpjt_ui (11)](https://github.com/user-attachments/assets/8496fd63-8158-4e0e-99ff-26181c9a121c)|

</div>
</details>

> ### 나만의 냉장고 페이지

<details>
<summary>나만의 냉장고 페이지 보기</summary>
<div markdown="1">

 |오늘의 메뉴 추천<br/>(추천 레시피)|냉장고 채우기1|냉장고 채우기2|냉장고 채우기3|냉장고 기반<br/>추천 레시피)|
 |:---:|:---:|:---:|:---:|:---:|
 |![pd_omcpjt_ui (13)](https://github.com/user-attachments/assets/b90acb0d-0007-4e63-b9c9-6f4195251ff5)|![pd_omcpjt_ui (14)](https://github.com/user-attachments/assets/1d086910-fa3f-401a-994d-739b2ff3a588)|![pd_omcpjt_ui (15)](https://github.com/user-attachments/assets/55d7eeb2-5f1b-415d-b98e-f633f23c653d)|![pd_omcpjt_ui (16)](https://github.com/user-attachments/assets/0dbb5e79-5024-45b0-8ace-cb15ea32f92e)|![pd_omcpjt_ui (17)](https://github.com/user-attachments/assets/b32984ce-a149-42d2-82bb-233c2da28dd9)|

</div>
</details>

> ### 레시피 상세 페이지

<details>
<summary>레시피 상세 페이지 보기</summary>
<div markdown="1">

 |레시피 상세|레시피 상세<br/>댓글 작성1|레시피 상세<br/>댓글 작성2|
 |:---:|:---:|:---:|
 |![pd_omcpjt_ui (18)](https://github.com/user-attachments/assets/d431cc1b-2ab4-4b77-8ada-bb0ce1947236)|![pd_omcpjt_ui (19)](https://github.com/user-attachments/assets/f1b68d01-d5bb-449a-bdc8-9482216d37da)|![pd_omcpjt_ui (20)](https://github.com/user-attachments/assets/d9fefd37-5d0b-4318-a774-c5b039224d9e)|

</div>
</details>

> ### 레시피 검색 페이지

<details>
<summary>레시피 검색 페이지 보기</summary>
<div markdown="1">

 |레시피 검색|레시피<br/>카테고리 검색1|레시피<br/>카테고리 검색2|레시피<br/>검색어 결과|
 |:---:|:---:|:---:|:---:|
 |![pd_omcpjt_ui (21)](https://github.com/user-attachments/assets/e2f97b66-5bae-4908-aada-7b3cabc7f9fa)|![pd_omcpjt_ui (23)](https://github.com/user-attachments/assets/1059ac7a-29a3-4db4-bad7-1f8de96b104f)|![pd_omcpjt_ui (24)](https://github.com/user-attachments/assets/008867f6-94c1-43be-911f-0519f4c3fc55)|![pd_omcpjt_ui (1)](https://github.com/user-attachments/assets/e4f436ef-cac6-4da7-b018-371a3d0d6dfa)|

</div>
</details>


## 기대효과
> ### 서비스 측면
 1. 통합된 요리 플랫폼
    * 다양한 레시피 정보 제공
    * 각 유저에게 적절한 레시피 추천
    * 다른 유저와 소통 가능한 커뮤니티
 2. 환경 보호
    * 가지고 있는 재료를 활용할 수 있는 레시피를 제공하여 재료가 방치되어 버려지는 것을 방지
> ### 비즈니스 측면
 1. 광고 : 쿠팡, 마켓컬리 등 재료 구매 시 오픈마켓과 연동하여 광고 수익 창출 가능
 2. 제휴 이벤트 : 데이터 분석을 통해 특정 시간대에,<br>특정 연령대에게 어떤 레시피가 인기 있는지 분석하여 대형마트와 제휴하여 다양한 이벤트 제공
 3. 구독 서비스 : 광고 제거, 셰프의 프리미엄 레시피를 제공

## 추후 개선사항
> ### 알고리즘 개선사항
 1. 가중치 부여 방식 변화 : TF-IDF가 아닌 다른 방식으로 주재료, 부재료에 가중치를 부여하는 방법이 필요함
 2. 클러스터링을 활용한 추천 : 유저에게 기피 재료를 입력받아 해당 재료가 포함된<br>레시피 클러스터를 제외하고 레시피 추천
 3. 협업 필터링 : 서비스가 운영되면 사용자의 활동 정보를 활용하여<br>레시피 우선순위 변경( ex: 사용자가 요리했으면 우선순위 ▽, 좋아요를 눌렀으면 우선순위 △ )
> ### 웹 개선사항
 1. Vue 적용 : 일부 페이지에 Vue, Axios를 적용하여 SPA 구현
 2. Youtube API 활용 : 해당 레시피와 관련된 요리 방법 영상 추천
 3. 기타 서비스 구현 : 좋아요 기능, 소셜 로그인, 타이머, 대댓글 등

## 기타
> ### DB ERD

<details>
<summary>DB ERD 보기</summary>
<div markdown="1">

|![image](https://user-images.githubusercontent.com/24910571/218047981-f60b46b5-cd9c-4691-8272-c5bfa0e10f72.png)|
|:--:|

</div>
</details>

> ### UI Flow

<details>
<summary>UI Flow 보기</summary>
<div markdown="1">

|![image](https://user-images.githubusercontent.com/24910571/218040627-71731674-4b7a-46ee-b502-83bd7959dd89.png)|
|:--:|

</div>
</details>

> ### 프로젝트 구조

<details>
<summary>프로젝트 구조 보기</summary>
<div markdown="1">
 
```
📦omc_pjt
┣ 📂venv_omcpjt
┃ ┣ 📂Include
┃ ┣ 📂Lib
┃ ┃ ┗ 📂site-packages
┃ ┣ 📂Scripts
┣ 📂OMC_project_review
┃ ┣ 📂.git
┃ ┣ 📂omc
┃ ┃ ┣ 📂migrations
┃ ┃ ┃ ┗ 📜__init__.py
┃ ┃ ┣ 📂templates
┃ ┃ ┃ ┗ 📂omc
┃ ┃ ┃ ┃ ┣ 📜comment_form.html
┃ ┃ ┃ ┃ ┣ 📜recipe_detail.html
┃ ┃ ┃ ┃ ┣ 📜recipe_list_view.html
┃ ┃ ┃ ┃ ┣ 📜recipe_recommend.html
┃ ┃ ┃ ┃ ┣ 📜refrigerator_list_view.html
┃ ┃ ┃ ┃ ┗ 📜refrigerator_list_vue.html
┃ ┃ ┣ 📜admin.py
┃ ┃ ┣ 📜apps.py
┃ ┃ ┣ 📜forms.py
┃ ┃ ┣ 📜models.py
┃ ┃ ┣ 📜tests.py
┃ ┃ ┣ 📜urls.py
┃ ┃ ┣ 📜views.py
┃ ┃ ┗ 📜__init__.py
┃ ┣ 📂OMC_PJT
┃ ┃ ┣ 📜asgi.py
┃ ┃ ┣ 📜mapping.json
┃ ┃ ┣ 📜model_utils.py
┃ ┃ ┣ 📜settings.py
┃ ┃ ┣ 📜urls.py
┃ ┃ ┣ 📜version.md
┃ ┃ ┣ 📜wsgi.py
┃ ┃ ┗ 📜__init__.py
┃ ┣ 📂scripts
┃ ┃ ┣ 📂jsons
┃ ┃ ┃ ┣ 📂category
┃ ┃ ┃ ┗ 📂page
┃ ┃ ┣ 📂search_app
┃ ┃ ┃ ┗ 📜create_bulk.py
┃ ┃ ┣ 📜category_add_scraper.py
┃ ┃ ┣ 📜category_scraper.py
┃ ┃ ┣ 📜combine_json_page.py
┃ ┃ ┣ 📜load_json_category.py
┃ ┃ ┣ 📜load_json_page.py
┃ ┃ ┣ 📜recipe_scraper.py
┃ ┃ ┣ 📜recipe_scraper_single_page_from_json.py
┃ ┃ ┗ 📜user_ingredient_add.py
┃ ┣ 📂static
┃ ┃ ┣ 📂assets
┃ ┃ ┣ 📂css
┃ ┃ ┗ 📂js
┃ ┣ 📂templates
┃ ┃ ┣ 📂partials
┃ ┃ ┃ ┣ 📜base.html
┃ ┃ ┃ ┣ 📜footer.html
┃ ┃ ┃ ┣ 📜measure.html
┃ ┃ ┃ ┗ 📜navbar.html
┃ ┃ ┣ 📜form_errors.html
┃ ┃ ┣ 📜index.html
┃ ┃ ┣ 📜login_view.html
┃ ┃ ┗ 📜signup_view.html
┃ ┣ 📜.gitignore
┃ ┣ 📜db.sqlite3
┃ ┣ 📜env_info.py
┃ ┣ 📜manage.py
┃ ┣ 📜README.md
┃ ┗ 📜req.txt
```

</div>
</details>


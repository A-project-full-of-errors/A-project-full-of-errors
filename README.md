# A-project-full-of-errors

## 커밋 컨벤션
<br>✨ feat : 새로운 기능 추가
<br>🐛 fix : 기능 수정, 버그 수정
<br>💡 chore : 오타 수정 및 새로운 기능이 추가되지 않고, 코드가 변경 된 경우 (주석 추가 및 수정 포함)
<br>📝 docs : 문서 수정 (readme 수정 시)
<br>🚚 build : 빌드 관련 파일 수정 및 삭제한 경우
<br>✅ test : 테스트 코드, 리팩터링 테스트 코드 추가(프로덕션 코드 변경 X)
<br>♻️ refactor : 코드 리팩터링
<br>🚑 hotfix : 긴급 수정

<hr>
<h2>ERD 설계</h2> 

![ERD](https://github.com/user-attachments/assets/9bebfdf6-cd90-4303-be00-11984355044a)

<hr>

## 회원가입 / 로그인 / 로그아웃 플로우 차트

1. 회원가입
- 사용자가 회원가입을 시작하고 회원정보를 입력함
- 서버는 회원 DB를 조회하여 중복 여부 등 유효성을 검사함
- 유효하지 않은 경우: 가입 불가 안내 + ID/PW 찾기 유도
- 유효한 경우: 회원 DB에 정보 저장 후 가입 완료

2. 로그인
- 사용자가 이메일과 비밀번호 입력
- 서버는 회원 DB에서 유효성 확인
- 유효하지 않으면: 로그인 실패 + ID/PW 찾기 유도
- 유효하면: JWT access/refresh 토큰 생성 → 로그인 성공

3. 로그아웃 
- 클라이언트가 로그아웃 요청 시 refresh token을 함께 전송
- 서버는 해당 refresh token을 blacklist에 저장 (더 이상 사용 불가)
- 로그아웃 완료 응답

4. 토큰 재발급
- access token 만료 시 클라이언트가 refresh token을 서버에 전송
- 서버는 refresh token의 유효성을 검사함
  → 유효하지 않으면: 401 에러 응답 → 다시 로그인 유도
  → 유효하면: 새로운 access token을 생성하여 응답

![Image](https://github.com/user-attachments/assets/1396737a-fdea-4423-8da3-00271085199b)
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

<iframe frameborder="0" style="width:100%;height:728px;" src="https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=%E1%84%8C%E1%85%A6%E1%84%86%E1%85%A9%E1%86%A8%20%E1%84%8B%E1%85%A5%E1%86%B9%E1%84%82%E1%85%B3%E1%86%AB%20%E1%84%83%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8B%E1%85%A5%E1%84%80%E1%85%B3&dark=auto#R%3Cmxfile%3E%3Cdiagram%20id%3D%22C5RBs43oDa-KdzZeNtuy%22%20name%3D%22Page-1%22%3E7Vxbd5s4EP41Oqd5cA93i0fjON100273pN2cfVSwYtMAokJO4v31K4EwBoRNksY4tl9sPBoumplvbhIG5jh6%2BkRRMv9CpjgEhjZ9AuY5MAzd0Bz%2BJSjLnAJ1SZjRYCqZSsJ18B%2BWRE1SF8EUpxVGRkjIgqRK9EkcY59VaIhS8lhluyNh9a4JmuEG4dpHYZN6E0zZXM7CGJb0P3Awmxd31h03H4lQwSxnks7RlDyukcwJMMeUEJYfRU9jHArhFXK5uVzehFf3zqfPf6e%2F0A%2Fvz%2B9f%2FxnkF7t4zimrKVAcs5dfGoVovPS%2BD67Q5fjK18PzeTKQc31A4ULKS86VLQsB4imXp%2FxJKJuTGYlROCmpHiWLeIrFbTT%2Bq%2BS5IiThRJ0Tf2LGltI40IIRTpqzKJSj%2BT3FjWo62zJhyZeSBfXxBj5T2h2iM8w2SENfaZXDAZMIM7rk51EcIhY8VB8OSbucrfhK2fMDKf5naNlsqmJyDtwRgGMwGQPXA64GJiPgaQBqGWUCoM3PEMeQj44l0dUbOiw1JMT9OA8Yvk5QJrNHDvuqNu5IzKSqdC4ObxaiNJXKTRkl9ysgCe4VKrSVIrvq7QFThp%2FWpNoUfTHqSAwWTkj%2BfCwRrRcwna%2Bh2dJ%2Bg7JUlmIfHG5a8dABN9aucLPhIbfgZgxGGnBtMPGAZwLPkrjJMcSJfHRkvw43LUbdVR%2BdjV%2B3%2Brb%2BYUPk%2F06uDxEAVkcAOH0CwDYa6vj61zFrw95ZHN%2FwlBV%2FNBbRmbuY3DGNYBayLeDp0g15hnBJfBTqYDR%2BH27I0Pp2Q7Za1KO1BEnh0w8ACE5XIJh9AsFRaKclfXVdAQcRhk0Rtt%2BH%2Fbt927%2FejMOHaO067Gjua1V5H3koVNg7t2g9q8y44Q%2BBlzl%2B91wc7GHd9vaYsZzeMXN4HY92KHTBjNEnZorHrCdL51k6xMHjAtcqKOIWWf1WBAsZSjyRPkGYJVewhNZ7LO1so298OM1y%2BkBruwL424u7XsOK0%2BwLHmZ1110f%2FbqsZrW9Pczzoi%2F3Y9xTjfgpTsgn6E2DB344E4cfnlsjnhUX4ZNYu847cXNd%2B7f2W7k5S1WcFPFDCNsR2jhAlFl2R5T12tO1FP31RlP3vGnt1TTXqIqWZ7yJ4IueZmKp8%2BNdSB79OaLs4xQxdItS3IKQt4KFXevrunYDFc4uQeEcRz1pd13WcPpt66oWNpT9E0%2B4K5EAF6ONIDAn0e0i3R4AqtHirezeNK2q4SvCAVQYPnyzRmKntVfj4DyOAXv2OLaiGj%2BKMGx3beH2W5%2FbLWnSQcdhVXa62zh8HD0qp2uPyoF9YsBp9qg%2B33zPAi%2BvxRxZsvGizNNkpQZNUfyV5dt7KMmcYd8lmdMsrC%2F5x8W3mywSaMCbZBkOzATdqKDXCmgPwAsh%2B44V8p4lR1bNGznNGL3T5MjpEgNUmWlDRYU6ZT9DqdG6sn6fnvlUg6Q1tuxcz1a9%2Bus7CXZetH6VeTgxagLvnTTZh3bfrg42Ny5QfEdxOt8UVsS%2BhqyJKEabYeUAMoJh18oc9rqxYaiqzJVIsaXGuI8Uj6zsBb8GMnu45LvKnvdmyRcqAtgBggd23eWeF%2F19gQcqei0ygCcVnTi%2FFuLNCi%2Fi8wliYI74qJY8ZZLUhOEPHhANEP%2BOFxGmgZ%2BzxIRGKFRwYZSyAUr58RZGFDJMY8TEWytKxpSreICmPxcpKzhivDZ%2Bz08P4lk%2BJg2hGCMJC3wUimu0sdxhxBYUD1JuTpyn7Smyx2UBiTsx8u%2BEpIHg3yaniPwM2mbOKGb%2BfINc8iHdLBQVBjEeFDBXnnWHoiBc5oNc6ygSPk7q%2FuMoSUJ8vUwZjn5cXnD2LyQmqfCH0zpvfknuzYQGg5mcZsrhIDPJgs%2FQfOkmS2KirzNUk09%2Bu1hpmbfIv59lfmHgk5DQ%2FI6MojgtUJ3drRwLhRwGU0TvP9DZ7Qc%2B3zHI9lFmX2f5txgxbDv%2FsX5wdlabSP6ctyF%2FjjDgxiiiyzBvVao2Qq7S5HxG1VlycvJ7VhHfQVCy7WZRteOgpHqD5OQGT27w5AZf6Aafk4LXthufHOOqDWj2nq03F6FPtbGQS9dd0G6v29WgqovUojSRlozlRk4JWwigC46jTnbrXam%2BgddcdTrQnZ%2BF5LdDqdcXydxj2fnZXR%2FGK%2FWRnTqiFC3XGBISxCxdu%2FI3QSiROqy%2Ff%2BvW%2Fmjhefz8IH%2BC0jJWU3mFsSh20p%2FqiVM9sYf1RGs6sGH78yh7xyNfcjKyV2SPITmvpQh61zX6N8sRXMXKx8nLnLzM%2FnkZ5PuYs20oGVurjyP0LIbVd%2FXhHsc%2F6rhG11S31%2Fcvisdc04aliUiMKSW0CYeXbaHaAyAMh8NqiFXsDdnpLhxX9Z8WnnhPfGSVL4znu%2F5bt%2BbUcfOynU97oB7o7kw9%2FGf5V355VVb%2BIaI5%2BR8%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E"></iframe>
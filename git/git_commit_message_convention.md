# Git 관리 전략

- Git Commit Message
    
    예시
    
    ```
    feat: Summarize changes in around 50 characters or less
    
    More detailed explanatory text, if necessary. Wrap it to about 72
    characters or so. In some contexts, the first line is treated as the
    subject of the commit and the rest of the text as the body. The
    blank line separating the summary from the body is critical (unless
    you omit the body entirely); various tools like `log`, `shortlog`
    and `rebase` can get confused if you run the two together.
    
    Explain the problem that this commit is solving. Focus on why you
    are making this change as opposed to how (the code explains that).
    Are there side effects or other unintuitive consequenses of this
    change? Here's the place to explain them.
    
    Further paragraphs come after blank lines.
    
     - Bullet points are okay, too
    
     - Typically a hyphen or asterisk is used for the bullet, preceded
       by a single space, with blank lines in between, but conventions
       vary here
    
    If you use an issue tracker, put references to them at the bottom,
    like this:
    
    Resolves: #123
    See also: #456, #789
    ```
    
    Title `Tag: Subject` 의 형식
    
    - Tag에 들어갈 수 있는 목록
        
        
        | 태그 이름 | 설명 |
        | --- | --- |
        | Feat | 새로운 기능 추가 |
        | Fix | 버그 수정 |
        | Design | CSS등 사용자 UI 디자인 수정 |
        | !BREAKING CHANGE | 커다란 API 변경의 경우 |
        | !HOTFIX | 급하게 치명적인 버그를 고쳐야하는 경우 |
        | Style | 코드 포멧팅, 세미콜론 누락, 코드 수정이 없는 경우 |
        | Refactor | 프로덕션 코드 리팩토링 |
        | Comment | 필요한 주석 추가 및 변경 |
        | Docs | 문서를 수정한 경우 |
        | Test | 테스트 추가, 테스트 리팩토링(프로덕션 코드 변경 X) |
        | Chore | 빌드 테스트 업데이트, 패키지 매니저를 설정하는 경우(프로덕션 코드 변경 X) |
        | Rename | 파일 혹은 폴더명 수정 혹은 옮기는 경우 |
        | Remove | 파일 삭제를 수행한 경우 |
    - Subject 작성 시 유의점
        - 제목은 최장 50글자, 마침표 및 특수기호는 지양
        - 영문 표기시, 첫 글자는 대문자로, 동사원형으로 작성
        - 제목은 개조식 구문, 즉 간결하고 요점적 서술로
    
    Body
    
    - 본문 작성 시 유의점
        - 본문은 줄당 72자 내로 작성
        - 최대한 상세히, 어떻게 변경했는지보다 무엇을 변경했는지 또는 왜 변경했는지를 설명
    
    Footer
    
    - 꼬리말 작성 시 유의점
        - 꼬리말은 `optional`이며, `이슈 트래커 ID`를 같이 작성
        - 꼬리말의 형식은 `유형: #이슈번호`의 형식을 사용
        - 여러 개 이슈 번호를 적을 때는 쉼표로 구분
        - `이슈 트래커 유형`의 목록
            - `Fixes`: 이슈 수정중(아직 해결 중)
            - `Resolves`: 이슈를 해결했을 때 사용
            - `Ref`: 참고할 이슈가 있을 때 사용
            - `Related to`: 해당 커밋에 관련된 이슈번호(아직 해결되지 않은 경우)


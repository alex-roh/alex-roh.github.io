# 블로그 에이전트 진입 안내

사용자와 한국어로 대화한다. 작업·공통 지침·현재 리더·담당·업무 메시지·결과의 정본은 Agent HQ 서버다.

- 본부: https://agent-hq.roheunyoung.workers.dev/
- 연결 절차: https://github.com/alex-roh/agent-hq#에이전트-연결
- 공통 도구: https://agent-hq-api.roheunyoung.workers.dev/client.mjs
- 프로젝트 ID: blog
- 레포: alex-roh/alex-roh.github.io

공통 도구를 레포 밖 임시 경로에 내려받고 실제 실행환경 신원(claude-local / claude-cloud / codex-local / codex-cloud)으로 연결한다. 이미 유효한 연결이 있으면 재사용한다. GitHub 권한 증명의 connect에는 --project blog --repo alex-roh/alex-roh.github.io를 사용한다. 연결 절차의 공개 proof 외에 비밀값을 공개 레포에 올리지 않는다.

먼저 bootstrap --agent ACTOR --project blog와 tasks --agent ACTOR --project blog를 실행해 활성 지침 전체·리더·배정을 읽는다. 기존 작업과 범위가 겹치지 않는지 확인하고, 실제 세션·담당 범위로 시작·주요 진행·업무 메시지·결과·검증 근거·남은 일·종료를 본부에 보고한다. 이전 기록은 이관 확인 전 삭제하지 않는다.

이 레포는 공개 콘텐츠를 배포한다. 본부의 비공개 지침 본문·대화·연결 키·개인정보를 블로그 콘텐츠나 빌드 산출물에 복제하지 않는다. 코드·검사·배포 근거는 GitHub에 연결한다. 게시글의 하위 AGENTS.md에 있는 콘텐츠 규칙을 함께 지킨다.

연결에 실패하면 실패 사실을 알리고 기록을 보존한다. 연결이나 작업 완료를 확인하기 전에 성공했다고 보고하지 않는다. 현재 지침은 본부에서 조회하고 이 파일에 복제하지 않는다.

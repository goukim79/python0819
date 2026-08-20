# Todoistly TRD

## 1. 기술 스택
- HTML5 semantic markup
- Tailwind CSS 3 via CDN Play script
- Vanilla JavaScript ES2020+
- Browser localStorage API
- 외부 빌드 도구와 서버 없이 `DemoPage.html` 직접 실행

## 2. 파일 구조
- `DemoPage.html`: 화면, Tailwind 스타일, 애플리케이션 로직
- `prd.md`: 제품 요구사항
- `trd.md`: 기술 요구사항
- `task.md`: 구현 체크리스트

## 3. 데이터 모델
```js
{
  id: Number,
  title: String,
  completed: Boolean,
  createdAt: String
}
```
저장 키는 `todoistly-items-v1`로 고정한다. 잘못된 저장 데이터는 빈 배열로 대체한다.

## 4. 화면 구성
- 헤더: 브랜드, 현재 날짜, 진행률
- 요약 영역: 전체/진행 중/완료 통계
- 입력 영역: 새 할 일 입력, 추가 버튼
- 도구 영역: 검색, 상태 필터, 완료 항목 삭제
- 목록 영역: 할 일 카드, 체크박스, 삭제 버튼
- 빈 상태 영역: 필터/검색에 맞는 안내 문구

## 5. 동작 규칙
- 공백만 입력된 제목은 등록하지 않는다.
- 등록 시 앞뒤 공백을 제거하고 입력창을 비운다.
- 목록 렌더링은 현재 검색어와 필터를 모두 적용한다.
- 모든 데이터 변경 후 localStorage에 저장하고 통계를 갱신한다.
- 진행률은 전체 항목이 0개면 0%, 그 외에는 완료/전체 비율을 반올림한다.
- 삭제 버튼은 해당 항목 하나만 삭제한다.

## 6. 접근성 및 반응형
- `header`, `main`, `section`, `form`, `ul` 등 의미 있는 요소를 사용한다.
- 아이콘 버튼에는 `aria-label`을 지정한다.
- 포커스 링을 숨기지 않고 Tailwind `focus-visible` 상태를 제공한다.
- 목록 카드는 작은 화면에서 제목과 삭제 버튼이 겹치지 않도록 flex/grid를 사용한다.

## 7. 검증
- HTML 파일을 브라우저로 열어 추가, 토글, 삭제, 필터, 검색을 확인한다.
- 새로고침 후 데이터 복원을 확인한다.
- 모바일 폭에서 레이아웃과 입력 동작을 확인한다.

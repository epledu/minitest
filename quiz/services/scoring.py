from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, MutableMapping, Optional

TRAIT_PRIORITY = [
    "Teto_M",
    "Teto_F",
    "Egen_M",
    "Egen_F",
    "테토남",
    "테토녀",
    "에겐남",
    "에겐녀",
]

TRAIT_SHARE_IMAGES = {
    "Teto_M": "/static/img/share-teto-m.png",
    "Teto_F": "/static/img/share-teto-f.png",
    "Egen_M": "/static/img/share-egen-m.png",
    "Egen_F": "/static/img/share-egen-f.png",
    "테토남": "/static/img/share-teto-m.png",
    "테토녀": "/static/img/share-teto-f.png",
    "에겐남": "/static/img/share-egen-m.png",
    "에겐녀": "/static/img/share-egen-f.png",
}

AFFILIATE_RECS = {
    "테토남": [
        {
            "title": "파워 에너지 보충 패키지",
            "description": "고강도 루틴을 버틸 에너지 음료 + 단백질 조합",
            "url": "https://example.com/partner/teto-m",
            "tag": "High Drive",
        },
    ],
    "테토녀": [
        {
            "title": "리더십 집중 케어 키트",
            "description": "집중력 강화 노트 + 프리미엄 커피 세트",
            "url": "https://example.com/partner/teto-f",
            "tag": "Lead",
        },
    ],
    "에겐남": [
        {
            "title": "심신 안정 티세트",
            "description": "차분한 리듬을 만드는 허브티 + 머그",
            "url": "https://example.com/partner/egen-m",
            "tag": "Calm",
        },
    ],
    "에겐녀": [
        {
            "title": "감정 리추얼 캔들",
            "description": "공감과 휴식을 돕는 아로마 캔들",
            "url": "https://example.com/partner/egen-f",
            "tag": "Empathy",
        },
    ],
}

DEFAULT_AFFILIATE = [
    {
        "title": "마음 회복 루틴 북",
        "description": "자기 이해를 돕는 워크북",
        "url": "https://example.com/partner/default",
        "tag": "Reset",
    }
]


def _safe_int(value: object) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def accumulate_scores(scores: Dict[str, int], delta_scores: Optional[Dict[str, object]]) -> Dict[str, int]:
    if not delta_scores:
        return scores
    for key, value in delta_scores.items():
        scores[key] = scores.get(key, 0) + _safe_int(value)
    return scores


def pick_best_trait(scores: Dict[str, int], priority: Iterable[str] = TRAIT_PRIORITY) -> Optional[str]:
    if not scores:
        return None
    max_score = max(scores.values())
    tied = {key for key, value in scores.items() if value == max_score}
    for key in priority:
        if key in tied:
            return key
    return sorted(tied)[0]


def get_share_image_url(request, trait_key: str, default_url: str) -> str:
    if trait_key in TRAIT_SHARE_IMAGES:
        candidate = TRAIT_SHARE_IMAGES[trait_key]
        if candidate.startswith("http"):
            return candidate
        return request.build_absolute_uri(candidate)
    return default_url


@dataclass
class SessionScoreService:
    session: MutableMapping
    key: str = "trait_scores"

    def get_scores(self) -> Dict[str, int]:
        return self.session.get(self.key, {})

    def add_scores(self, delta_scores: Optional[Dict[str, object]]) -> Dict[str, int]:
        scores = dict(self.get_scores())
        scores = accumulate_scores(scores, delta_scores)
        self.session[self.key] = scores
        try:
            self.session.modified = True
        except AttributeError:
            pass
        return scores

    def best_trait(self) -> Optional[str]:
        return pick_best_trait(self.get_scores())

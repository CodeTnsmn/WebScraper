# Git Kuralları

## Branch
- `main` korunur, doğrudan push yok.
- Feature: `feature/<spec-no>-<kisa-ad>` · Fix: `fix/<kisa-ad>`.

## Commit
- Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`.
- Her commit tek mantıksal değişiklik; spec/AC'ye referans verir.

## PR
- Açıklama: ne/neden + kriter↔test tablosu + doğrulama kanıtı.
- Bağımsız REVIEW geçmeden merge yok.

## Gizli/hariç tutulan dosyalar
- `AGENTS.md` bilinçli olarak `.gitignore`'da — bkz. AGENTS.md üstündeki not.
- `.env`, `*.db`, `output/` (export edilen CSV/Excel) repoya girmez.
